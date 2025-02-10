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
    QgsProcessingOutputLayerDefinition,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
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


from .manning_roughness_calculator import ManningRoughnessCalculator

class ManningRoughnessAlgorithm(QgsProcessingAlgorithm):
    """QGIS Processing Algorithm for Manning Roughness"""

    def name(self):
        return "manningroughness"

    def displayName(self):
        return "Manning Roughness Generator"  

    def shortHelpString(self):
        return QCoreApplication.translate(
            "Processing",
            "Generates Manning roughness raster from ESA WorldCover data, "
            "allowing for classification based on predefined roughness lookup tables."
        )

    def createInstance(self):
        return ManningRoughnessAlgorithm()

    def initAlgorithm(self, config=None):
        self.roughness_classes = ["Low", "Medium", "High"]
        self.lc_pixel_size = 0.000083333333333 

        # Step 1: Add AOI parameter
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                "aoi",
                "Area of Interest",
                types=[QgsProcessing.TypeVectorPolygon],
                defaultValue=None,
            )
        )

        # Step 2: Add Roughness Class Selection
        param = QgsProcessingParameterEnum(
            "ROUGHNESS_CLASS",
            "Roughness Class",
            options=self.roughness_classes,
            allowMultiple=False,
            defaultValue=1,
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

        # Step 3: Add ESA WorldCover Output (Optional)
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                "EsaWorldcoverAOI",
                "ESA WorldCover 2021",
                optional=True,
                createByDefault=False,
                defaultValue=None,
            )
        )

        # Step 4: Add Manning Roughness Output
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                "ManningRoughness",
                "Manning's Roughness (Raster)",
                optional=True,
                createByDefault=True,
                defaultValue=None,
            )
        )

        # Step 5: Add Manning Roughness Vector Output (Optional)
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                "ManningRoughnessVector",
                "Manning's Roughness (Vector)",
                optional=True,
                createByDefault=False,
                defaultValue=None,
            )
        )


#    def processAlgorithm(self, parameters, context, model_feedback):
#        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
#
#        # Step 1: Extract AOI extent
#        aoi_layer = QgsProcessingUtils.mapLayerFromString(parameters["aoi"], context)
#        if aoi_layer is None:
#            raise QgsProcessingException("Invalid AOI layer.")
#
#        extent = aoi_layer.extent()
#        feedback.pushInfo(f"AOI extent extracted: {extent.toString()}")
#
#        # Step 2: Ensure extent_esa is always assigned, avoiding UnboundLocalError
#        extent_esa = None  
#
#        # Extract AOI CRS
#        source_crs = aoi_layer.crs()
#        target_crs = QgsCoordinateReferenceSystem("EPSG:4326")
#        if source_crs.authid() != "EPSG:4326":
#            transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
#            reprojected_extent = transform.transformBoundingBox(extent)
#            feedback.pushInfo(f"AOI reprojected to EPSG:4326: {reprojected_extent.toString()}")
#        else:
#            reprojected_extent = extent  # Already in EPSG:4326
#
#            # Assign `extent_esa` after reprojection to avoid unbound errors
#            extent_esa = (
#                    reprojected_extent.xMinimum() - 2 * self.lc_pixel_size,
#                    reprojected_extent.yMinimum() - 2 * self.lc_pixel_size,
#                    reprojected_extent.xMaximum() + 2 * self.lc_pixel_size,
#                    reprojected_extent.yMaximum() + 2 * self.lc_pixel_size,
#                    )
#
#            # Debugging: Ensure `extent_esa` is assigned before using it
#            feedback.pushInfo(f"Buffered ESA extent: {extent_esa}")
#
#            # Check if extent_esa was correctly assigne
#            if extent_esa is None:
#                raise QgsProcessingException("Error: extent_esa was not assigned before usage.")
#
#
#        # Step 4: Process ESA WorldCover Raster
#
#        esa_output = parameters.get("EsaWorldcoverAOI", QgsProcessing.TEMPORARY_OUTPUT)
#
#        gdal_output = processing.run(
#                "gdal:cliprasterbyextent",
#                {
#                    "INPUT": os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt"),
#                    "PROJWIN": f"{extent_esa[0]},{extent_esa[2]},{extent_esa[1]},{extent_esa[3]} [EPSG:4326]",
#                    "OUTPUT": esa_output
#                    },
#                context=context, feedback=feedback,
#                is_child_algorithm=True
#                )
#
#        if "OUTPUT" not in gdal_output or not os.path.exists(gdal_output["OUTPUT"]):
#            raise QgsProcessingException(f"ESA raster processing failed. GDAL Output: {gdal_output}")
#        
#        esa_raster = gdal_output["OUTPUT"]
#        feedback.pushInfo(f"ESA WorldCover raster processed at: {esa_raster}")
#
#        # Ensure the function returns a dictionary, as required by QGIS
#        return {
#                "EsaWorldcoverAOI": esa_raster  # Always return the ESA raster path
#                }


    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)

        # Step 1: Load AOI layer
        aoi_layer = QgsProcessingUtils.mapLayerFromString(parameters["aoi"], context)
        if aoi_layer is None or not isinstance(aoi_layer, QgsVectorLayer):
            raise QgsProcessingException("Invalid AOI vector layer.")

        feedback.pushInfo(f"AOI original CRS: {aoi_layer.crs().authid()}")

        # Step 2: Always reproject AOI to EPSG:4326
        target_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transformed_layer = processing.run(
                "native:reprojectlayer",
                {
                    "INPUT": aoi_layer,
                    "TARGET_CRS": target_crs,
                    "OUTPUT": "memory:"  # Keep the result in memory
                    },
                context=context,
                feedback=feedback
                )["OUTPUT"]

        if transformed_layer is None:
            raise QgsProcessingException("Failed to reproject AOI to EPSG:4326.")

        #Extract extent from the reprojected layer
        reprojected_extent = transformed_layer.extent()
        feedback.pushInfo(f"AOI reprojected extent (EPSG:4326): {reprojected_extent.toString()}")

        # Assign `extent_esa` after reprojection
        if not hasattr(self, "lc_pixel_size") or self.lc_pixel_size is None:
            raise QgsProcessingException("lc_pixel_size is not defined!")

        extent_esa = (
                reprojected_extent.xMinimum() - 2 * self.lc_pixel_size,
                reprojected_extent.yMinimum() - 2 * self.lc_pixel_size,
                reprojected_extent.xMaximum() + 2 * self.lc_pixel_size,
                reprojected_extent.yMaximum() + 2 * self.lc_pixel_size,
                )
        feedback.pushInfo(f"Buffered ESA extent: {extent_esa}")
        
        # Step 3: Process ESA WorldCover Raster
        esa_output = parameters.get("EsaWorldcoverAOI", QgsProcessing.TEMPORARY_OUTPUT)

        gdal_output = processing.run(
                "gdal:cliprasterbyextent",
                {
                    "INPUT": os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt"),
                    "PROJWIN": f"{extent_esa[0]},{extent_esa[2]},{extent_esa[1]},{extent_esa[3]} [EPSG:4326]",
                    "OUTPUT": esa_output,
                    },
                context=context, feedback=feedback,
                is_child_algorithm=True
                )

        if "OUTPUT" not in gdal_output or not os.path.exists(gdal_output["OUTPUT"]):
            raise QgsProcessingException(f"ESA raster processing failed. GDAL Output: {gdal_output}")

        esa_raster = gdal_output["OUTPUT"]
        feedback.pushInfo(f"ESA WorldCover raster processed at: {esa_raster}")

        # Step 4: Process Manning Roughness Calculation
        feedback.pushInfo("Starting Manning Roughness calculation...")
        results = self.processManningRoughness(esa_raster, parameters, context, feedback)

        feedback.pushInfo("Manning Roughness calculation completed.")
        # Step 5: Return Results (Ensure ESA & Roughness are both included)
        results["EsaWorldcoverAOI"] = esa_raster
        return results


    def processManningRoughness(self, esa_raster, parameters, context, feedback):
        # Step 5: Load Manning Roughness Lookup Table
        roughness_lookup = ["low_n.csv", "med_n.csv", "high_n.csv"]
        selected_lookup = roughness_lookup[parameters["ROUGHNESS_CLASS"]]
        lookup_file = os.path.join(os.path.dirname(__file__), "lookups", selected_lookup)

        lookup_layer = QgsVectorLayer(f"file://{lookup_file}?delimiter=,", "ManningRoughnessLookup", "delimitedtext")

        if not lookup_layer.isValid():
            raise QgsProcessingException(f"Failed to load Manning Roughness lookup table: {lookup_file}")

        feedback.pushInfo(f"Manning Roughness lookup table loaded from: {lookup_file}")

        # Step 6: Compute Manning Roughness
        feedback.pushInfo(f"Passing ESA raster to calculator: {esa_raster}")

        if not os.path.exists(esa_raster):
            raise QgsProcessingException(f"ESA raster missing before passing to calculator: {esa_raster}")

        calculator = ManningRoughnessCalculator(
                parameters, context, feedback,
                esa_raster, lookup_layer,
                parameters["ManningRoughness"],
                parameters.get("ManningRoughnessVector", None)
                )

        results = calculator.run()

# Need to add the ManningRoughnessVector processing. for now, it does not produce output.
        # Ensure the vector output is present in results
        if "ManningRoughnessVector" in results and results["ManningRoughnessVector"]:
            feedback.pushInfo(f"Manning Roughness Vector created at: {results['ManningRoughnessVector']}")

            feedback.pushInfo("Manning Roughness computation completed.")
            return results

        # Ensure output exists
        output_raster = parameters["ManningRoughness"]
#        if isinstance(output_raster, QgsProcessingOutputLayerDefinition):
#            output_raster = str(output_raster)  # Convert to string, even if it's an object
#
#            if not os.path.exists(output_raster):
#                print(f"WARNING: Manning Roughness raster might not have been created: {output_raster}")
#

        feedback.pushInfo(f"Manning Roughness raster saved at: {output_raster}")
        feedback.pushInfo("Manning Roughness Algorithm completed successfully.")

        return results
