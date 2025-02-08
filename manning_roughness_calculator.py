import os
import processing
from qgis.core import QgsProcessingException, QgsProcessingUtils
from .utils import (
    clipRasterByExtent,
    generate_manning_exprs,
    perform_raster_math,
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
        land_cover_vrt = os.path.join(os.path.dirname(__file__), "land_cover.vrt")
        self.outputs["ClippedLandCover"] = clipRasterByExtent(
            land_cover_vrt, extent, processing.TEMPORARY_OUTPUT, self.context, self.feedback
        )

        self.feedback.setCurrentStep(2)
        if self.feedback.isCanceled():
            return {}

        # Step 3: Generate Manning Roughness Raster
        manning_exprs = generate_manning_exprs("lookups/manning_lookup.csv")
        input_dict = {"input_a": self.outputs["ClippedLandCover"], "band_a": 1}

        self.outputs["ManningRoughness"] = perform_raster_math(
            manning_exprs, input_dict, self.context, self.feedback, processing.TEMPORARY_OUTPUT
        )

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
