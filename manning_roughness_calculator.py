import os
import sys
import processing

from qgis.core import QgsProcessingException, QgsProcessingUtils
from .utils import (
    clipRasterByExtent,
#   generate_manning_exprs,
    perform_raster_math,
    load_manning_lookup,
    gdalPolygonize,
    apply_style,
)

class ManningRoughnessCalculator:
    def __init__(self, parameters, context, feedback):
        self.parameters = parameters
        self.context = context
        self.feedback = feedback
        self.outputs = {}
        self.results = {}

    def run(self):
        """Main processing logic for Manning Roughness calculation"""
        self.feedback.setCurrentStep(1)
        if self.feedback.isCanceled():
            return {}

        # Step 1: Extract AOI extent
        aoi_layer = QgsProcessingUtils.mapLayerFromString(self.parameters["aoi"], self.context)
        if aoi_layer is None:
            raise QgsProcessingException("Invalid Area of Interest (AOI) layer")

        extent = aoi_layer.extent()
        print(f"AOI extent: {extent}")

        return {"OUTPUT": "Processing complete"}

        # Step 2: Clip Land Cover Raster
#        land_cover_vrt = os.path.join(os.path.dirname(__file__), "land_cover.vrt")
#        self.outputs["clipped_esa_worldcover_2021"] = clipRasterByExtent(
#            land_cover_vrt, extent, processing.TEMPORARY_OUTPUT, self.context, self.feedback
#        )
#
#        self.feedback.setCurrentStep(2)
#        if self.feedback.isCanceled():
#            return {}

        # Step 2: Clip Land Cover Raster 
        
        clipped_esa_worldcover_2021 = clipRasterByExtent(
                os.path.join(os.path.dirname(__file__), "land_cover.vrt"),
                extent,
                self.parameters["ManningRoughness"],  # Save to a real output path
                self.context,
                self.feedback,
                )
        self.outputs["clipped_esa_worldcover_2021"] = clipped_esa_worldcover_2021

        
        # Ensure QGIS registers the raster properly before continuing
        clipped_raster_layer = QgsProcessingUtils.mapLayerFromString(clipped_esa_worldcover_2021, self.context)
        if clipped_raster_layer is None:
            raise QgsProcessingException("QGIS failed to load clipped land cover raster.")

        # Step 3: Generate Manning Roughness Raster
#        manning_exprs = generate_manning_exprs("lookups/manning_lookup.csv")
#        input_dict = {"input_a": self.outputs["clipped_esa_worldcover_2021"], "band_a": 1}
#
#        self.outputs["ManningRoughness"] = perform_raster_math(
#            manning_exprs, input_dict, self.context, self.feedback, processing.TEMPORARY_OUTPUT
        )

        # Step 3: Load Lookup Table as Vector Layer

        lookup_layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "lookups/manning_lookup.csv"),
                              "ManningRoughnessLookup", "ogr")
        if not lookup_layer.isValid():
            raise QgsProcessingException("Failed to load Manning Roughness lookup table")


        # Step 4: Perform Join (like Curve Number)

        alg_params = {
                "DISCARD_NONMATCHING": False,
                "FIELD": "raster_value",  # Land cover field in raster
                "FIELDS_TO_COPY": ["n"],  # Manning roughness coefficient
                "FIELD_2": "lc",  # Land cover field in lookup
                "INPUT": self.outputs["clipped_esa_worldcover_2021"],  # The clipped raster
                "INPUT_2": lookup_layer,  # Lookup table
                "METHOD": 1,
                "PREFIX": "",
                "OUTPUT": self.parameters["ManningRoughness"],
                }

        # Load Clipped Raster Layer into QGIS before joining
        clipped_raster_layer = QgsProcessingUtils.mapLayerFromString(self.outputs["clipped_esa_worldcover_2021"], self.context)
        if clipped_raster_layer is None:
            raise QgsProcessingException("Clipped land cover raster layer could not be loaded in QGIS.")

        # Join Lookup Tabl
        self.outputs["ManningRoughness"] = processing.runAndLoadResults(
                "native:joinattributestable", alg_params, context=self.context, feedback=self.feedback
                )["OUTPUT"]

        self.feedback.setCurrentStep(3)
        if self.feedback.isCanceled():
            return {}

        # Step 4: Convert Roughness Raster to Vector (Optional)
        if self.parameters.get("ManningRoughnessVector", None):
            self.outputs["ManningRoughnessVector"] = gdalPolygonize(
                self.outputs["ManningRoughness"], "roughness", self.parameters["ManningRoughnessVector"], self.context, self.feedback
            )
            apply_style(self.outputs["ManningRoughnessVector"], "manning_roughness_vector.qml", self.context)
            self.results["ManningRoughnessVector"] = self.outputs["ManningRoughnessVector"]

        # Step 5: Apply Raster Styling
        apply_style(self.outputs["ManningRoughness"], "manning_roughness_raster.qml", self.context)
        self.results["ManningRoughness"] = self.outputs["ManningRoughness"]

        return self.results
