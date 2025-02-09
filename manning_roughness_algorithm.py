# -*- coding: utf-8 -*-

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
import pandas as pd
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsVectorLayer,
    QgsProcessingParameterBoolean,
    QgsVectorFileWriter,
    QgsProcessingUtils,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterDefinition,
)
from qgis.PyQt.QtCore import QCoreApplication
from .utils import (
    clipRasterByExtent,
    perform_raster_math,
    gdalPolygonize,
    apply_style,
)

class ManningRoughnessAlgorithm(QgsProcessingAlgorithm):
    """QGIS Processing Algorithm for Manning Roughness"""

    def initAlgorithm(self, config=None):
        self.roughness_classes = ["Low", "Medium", "High"]

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "aoi",
                "Area of Interest",
                types=[QgsProcessing.TypeVectorPolygon],
                defaultValue=None,
            )
        )

        param = QgsProcessingParameterEnum(
            "ROUGHNESS_CLASS",
            "Roughness Class",
            options=self.roughness_classes,
            allowMultiple=False,
            defaultValue=1,
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

        self.addParameter(
                QgsProcessingParameterRasterDestination(
                    "EsaWorldcoverAOI",
                    "ESA WorldCover for AOI",
                    optional=True,
                    createByDefault=False,
                    defaultValue=None,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                "ManningRoughness",
                "Manning Roughness Coefficient",
                optional=True,
                createByDefault=True,
                defaultValue=None,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                "ManningRoughnessVector",
                "Manning Roughness (Vectorized)",
                optional=True,
                createByDefault=False,
                defaultValue=None,
            )
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        calculator = ManningRoughnessCalculator(parameters, context, feedback)
        return calculator.run()

    def name(self):
        return "manningroughness"

    def displayName(self):
        return QCoreApplication.translate("Processing", "Manning Roughness Generator")

    def shortHelpString(self):
        return QCoreApplication.translate("Processing", "Generates Manning roughness raster from ESA WorldCover data.")

    def createInstance(self):
        return ManningRoughnessAlgorithm()

class ManningRoughnessCalculator:
    def __init__(self, parameters, context, feedback):
        """Initialize Manning Roughness Calculator"""
        self.parameters = parameters
        self.context = context
        self.feedback = feedback
        self.outputs = {}  # Store intermediate and final outputs
        self.results = {}  # Store additional processing results
        self.lookup_folder = os.path.join(os.path.dirname(__file__), "lookups")
        
        # Define ESA WorldCover VRT path
        self.esa_worldcover_2021_vrt = os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt")

        # Verify the ESA WorldCover VRT file exists before using it
        if not os.path.exists(self.esa_worldcover_2021_vrt):
            raise QgsProcessingException(f"Missing ESA WorldCover VRT file: {self.esa_worldcover_2021_vrt}")

        self.feedback.pushInfo(f"ESA WorldCover VRT found at: {self.esa_worldcover_2021_vrt}")

    def run(self):
        """Main processing logic for Manning Roughness calculation"""
        self.feedback.setCurrentStep(1)
        if self.feedback.isCanceled():
            return {}

        # Step 1: Extract AOI extent
        self.feedback.pushInfo("Extracting AOI extent...")
        aoi_layer = QgsProcessingUtils.mapLayerFromString(self.parameters["aoi"], self.context)
        if aoi_layer is None:
            raise QgsProcessingException("Invalid Area of Interest (AOI) layer")

        extent = aoi_layer.extent()
        print(f"AOI extent: {extent}")
        self.feedback.pushInfo(f"AOI extent extracted: {extent.toString()}")

        # Step 2: Generate ESA WorldCover for AOI only if output is requested
        if self.parameters.get("EsaWorldcoverAOI"):
            self.feedback.pushInfo("Generating ESA WorldCover raster for AOI...")

            # Clip the ESA WorldCover VRT based on the AOI extent
            clipped_esa_worldcover_2021 = clipRasterByExtent(
                self.esa_worldcover_2021_vrt, extent, self.parameters["EsaWorldcoverAOI"], self.context, self.feedback
            )

            if not clipped_esa_worldcover_2021:
                self.feedback.reportError("Failed to generate ESA WorldCover raster for AOI.")
                raise QgsProcessingException("Failed to generate ESA WorldCover raster for AOI.")

            self.outputs["clipped_esa_worldcover_2021"] = clipped_esa_worldcover_2021
            self.feedback.pushInfo(f"ESA WorldCover raster saved at: {clipped_esa_worldcover_2021}")

        else:
            # If no raster is requested, handle it gracefully
            self.feedback.pushInfo("Skipping ESA WorldCover raster generation as no output is requested.")
            self.outputs["clipped_esa_worldcover_2021"] = None



        # Step 3: Select the correct lookup file based on ROUGHNESS_CLASS
        roughness_lookup = ["low_n.csv", "med_n.csv", "high_n.csv"]
        selected_lookup = roughness_lookup[self.parameters["ROUGHNESS_CLASS"]]
        lookup_file = os.path.join(self.lookup_folder, selected_lookup)

        #lookup_layer = QgsVectorLayer(lookup_file, "ManningRoughnessLookup", "ogr")
        #if not lookup_layer.isValid():
        #    raise QgsProcessingException("Failed to load Manning Roughness lookup table")

        # Load lookup table as a QGIS vector layer using 'delimitedtext' if it's a CSV
        lookup_uri = f"file://{lookup_file}?delimiter=,"
        lookup_layer = QgsVectorLayer(lookup_uri, "ManningRoughnessLookup", "delimitedtext")

        if not lookup_layer.isValid():
            raise QgsProcessingException(f"Failed to load Manning Roughness lookup table: {lookup_file}")


        if not self.outputs.get("clipped_esa_worldcover_2021"):
            raise QgsProcessingException("ESA WorldCover raster is missing. Ensure clipping was executed successfully.")
        
        alg_params = {
                "DISCARD_NONMATCHING": False,
                "FIELD": "raster_value",
                "FIELDS_TO_COPY": ["n"],
                "FIELD_2": "lc",
                "INPUT": self.outputs["clipped_esa_worldcover_2021"],  # Use the correct reference
                "INPUT_2": lookup_layer,
                "METHOD": 1,
                "PREFIX": "",
                "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
                }

        
        # Step 4: Generate the raster math expression for Manning roughness
        exprs = " + ".join([f"(A == {feature['lc']}) * {feature['n']}" for feature in lookup_layer.getFeatures()])

        # Apply raster calculation using the generated expression
        input_dict = {"input_a": clipped_esa_worldcover_2021, "band_a": 1}
        manning_roughness = perform_raster_math(
                exprs, input_dict, self.context, self.feedback, no_data=-9999, out_data_type=5,
                output=self.parameters["ManningRoughness"]
                )

        
        # Step 5: Polygonize (optional)
        if self.parameters.get("ManningRoughnessVector"):
            self.outputs["ManningRoughnessVector"] = gdalPolygonize(
                manning_roughness, "roughness", self.parameters["ManningRoughnessVector"], self.context, self.feedback
            )
            apply_style(self.outputs["ManningRoughnessVector"], "manning_roughness_vector.qml", self.context)
            self.results["ManningRoughnessVector"] = self.outputs["ManningRoughnessVector"]

        # Step 6: Apply style and return results
        apply_style(manning_roughness, "manning_roughness_raster.qml", self.context)
        self.results["ManningRoughness"] = manning_roughness

        return self.results
