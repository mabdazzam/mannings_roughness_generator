
"""
Manning's Roughness Generator - A QGIS Plugin
Generates Manning's roughness coefficient layers for hydrological modeling.

Created on: 2025-02-08
Copyright: (C) 2025 by Abdullah Azzam
Email: mabdazzam@outlook.com

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

__author__ = "Abdullah Azzam"
__date__ = "2025-02-08"
__copyright__ = "(C) 2025 by Abdullah Azzam"

import os
import processing
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingUtils,
    QgsVectorLayer,
    QgsApplication,
    QgsRasterLayer,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsProcessingOutputLayerDefinition,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterDefinition,
    QgsProcessingOutputLayerDefinition,
)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QTimer
from .mannings_roughness_calculator import ManningsRoughnessCalculator

class ManningsRoughnessAlgorithm(QgsProcessingAlgorithm):
    """QGIS Processing Algorithm for Mannings Roughness"""

    def name(self):
        return "manningroughness"

    def displayName(self):
        return "Mannings Roughness Generator"

    def shortHelpString(self):
        return QCoreApplication.translate(
            "Processing",
            "Generates Mannings roughness raster from ESA WorldCover data, "
            "allowing for classification based on predefined roughness lookup tables."
        )

    def createInstance(self):
        return ManningsRoughnessAlgorithm()

    def initAlgorithm(self, config=None):
        self.roughness_classes = ["Low", "Medium", "High"]
        self.lc_pixel_size = 0.000083333333333

        # add aoi parameter
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "aoi",
                "Area of Interest",
                types=[QgsProcessing.TypeVectorPolygon],
                defaultValue=None,
            )
        )

        # add roughness class selection
        param = QgsProcessingParameterEnum(
            "ROUGHNESS_CLASS",
            "Roughness Class",
            options=self.roughness_classes,
            allowMultiple=False,
            defaultValue=1,
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

        # add esa worldcover output
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                "EsaWorldcoverAOI",
                "ESA WorldCover 2021",
                optional=True,
                createByDefault=False,
                defaultValue=None,
            )
        )

        # add mannings roughness output
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                "ManningsRoughness",
                "Manning's Roughness (Raster)",
                optional=True,
                createByDefault=True,
                defaultValue=None,
            )
        )
    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)

        # load aoi
        aoi_layer = QgsProcessingUtils.mapLayerFromString(parameters["aoi"], context)
        if aoi_layer is None or not isinstance(aoi_layer, QgsVectorLayer):
            raise QgsProcessingException("invalid aoi vector layer.")

        feedback.pushInfo(f"aoi original crs: {aoi_layer.crs().authid()}")

        # reproject aoi to epsg:4326
        target_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transformed_layer = processing.run(
                "native:reprojectlayer",
                {
                    "INPUT": aoi_layer,
                    "TARGET_CRS": target_crs,
                    "OUTPUT": "memory:"
                    },
                context=context,
                feedback=feedback
                )["OUTPUT"]

        if transformed_layer is None:
            raise QgsProcessingException("failed to reproject aoi to epsg:4326.")

        # extract extent
        reprojected_extent = transformed_layer.extent()
        feedback.pushInfo(f"aoi reprojected extent (epsg:4326): {reprojected_extent.toString()}")

        if not hasattr(self, "lc_pixel_size") or self.lc_pixel_size is None:
            raise QgsProcessingException("lc_pixel_size is not defined!")

        extent_esa = (
                reprojected_extent.xMinimum() - 2 * self.lc_pixel_size,
                reprojected_extent.yMinimum() - 2 * self.lc_pixel_size,
                reprojected_extent.xMaximum() + 2 * self.lc_pixel_size,
                reprojected_extent.yMaximum() + 2 * self.lc_pixel_size,
                )
        feedback.pushInfo(f"buffered esa extent: {extent_esa}")

        # clip esa worldcover
        esa_output = parameters.get("EsaWorldcoverAOI", QgsProcessing.TEMPORARY_OUTPUT)
        gdal_output = processing.run(
                "gdal:cliprasterbyextent",
                {
                    "INPUT": os.path.normpath(os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt")),
                    "PROJWIN": f"{extent_esa[0]},{extent_esa[2]},{extent_esa[1]},{extent_esa[3]} [EPSG:4326]",
                    "OUTPUT": esa_output,
                    },
                context=context, feedback=feedback,
                is_child_algorithm=True
                )

        if "OUTPUT" not in gdal_output or not os.path.exists(gdal_output["OUTPUT"]):
            raise QgsProcessingException("esa raster processing failed.")

        esa_raster = gdal_output["OUTPUT"]
        feedback.pushInfo(f"esa worldcover raster processed at: {esa_raster}")


        feedback.pushInfo("starting mannings roughness calculation...")

        roughness_lookup = ["low_n.csv", "med_n.csv", "high_n.csv"]
        selected_lookup = roughness_lookup[parameters["ROUGHNESS_CLASS"]]
        lookup_file = os.path.normpath(os.path.join(os.path.dirname(__file__), "lookups", selected_lookup))

        feedback.pushInfo(f"loading mannings roughness lookup table from: {lookup_file}")

        if not os.path.exists(lookup_file):
            raise QgsProcessingException(f"lookup table not found: {lookup_file}")

        lookup_values = []
        with open(lookup_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    try:
                        lc_value = int(parts[0])
                        n_value = float(parts[1])
                        lookup_values.append((lc_value, n_value))
                    except ValueError:
                        feedback.pushWarning(f"skipping invalid row in lookup file: {line.strip()}")

        if not lookup_values:
            raise QgsProcessingException(f"lookup table {selected_lookup} is empty or malformed.")

        feedback.pushInfo(f"loaded {len(lookup_values)} land cover to roughness mappings.")

        exprs = " + ".join([f"(A == {lc}) * {n}" for lc, n in lookup_values])
        feedback.pushInfo(f"generated raster math expression: {exprs}")

        input_dict = {"input_a": esa_raster, "band_a": 1}
        roughness_output = parameters.get("ManningsRoughness", QgsProcessing.TEMPORARY_OUTPUT)

        gdal_result = processing.run(
                "gdal:rastercalculator",
                {
                    "FORMULA": exprs,
                    "INPUT_A": input_dict["input_a"],
                    "BAND_A": input_dict["band_a"],
                    "NO_DATA": -9999,
                    "RTYPE": 5,
                    "OUTPUT": roughness_output,
                    },
                context=context, feedback=feedback,
                is_child_algorithm=True
                )

        if "OUTPUT" not in gdal_result or not os.path.exists(gdal_result["OUTPUT"]):
            raise QgsProcessingException("mannings roughness raster was not created!")

        mannings_raster = gdal_result["OUTPUT"]
        feedback.pushInfo(f"mannings roughness raster saved at: {mannings_raster}")
        feedback.pushInfo("applying styling...")

        esa_style_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.qml"))
        roughness_style_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "mannings_n.qml"))

        ## renaming and styling 
        # check if esa output is defined to avoid keyerror
        esa_output_selected = "EsaWorldcoverAOI" in parameters and parameters["EsaWorldcoverAOI"] not in [None, ""]

        # normalize raster paths to avoid OS issues
        esa_raster = os.path.normpath(esa_raster) if esa_output_selected else None
        mannings_raster = os.path.normpath(mannings_raster) if "ManningsRoughness" in parameters and parameters["ManningsRoughness"] not in [None, ""] else None

        # only apply esa styling if the user selected an output
        if esa_output_selected:
            if os.path.exists(esa_raster):
                esa_layer = QgsRasterLayer(esa_raster, "", "gdal")
                if esa_layer.isValid():
                    esa_layer.setName("ESA WorldCover 2021")
                    esa_style_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.qml"))
                    if os.path.exists(esa_style_path):
                        esa_layer.loadNamedStyle(esa_style_path)
                    esa_layer.triggerRepaint()
                    QgsProject.instance().addMapLayer(esa_layer)

        # apply styling to mannings n (independent of esa) 
        if mannings_raster:
            if os.path.exists(mannings_raster):
                roughness_layer = QgsRasterLayer(mannings_raster, "", "gdal")
                if roughness_layer.isValid():
                    roughness_layer.setName("Manning's n")
                    roughness_style_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "mannings_n.qml"))
                    if os.path.exists(roughness_style_path):
                        roughness_layer.loadNamedStyle(roughness_style_path)
                    roughness_layer.triggerRepaint()
                    QgsProject.instance().addMapLayer(roughness_layer)

        feedback.pushInfo("styling applied. returning results.")

        # return only the outputs that were selected
        return {
            "EsaWorldcoverAOI": esa_raster,
            "ManningsRoughness": mannings_raster
        }

