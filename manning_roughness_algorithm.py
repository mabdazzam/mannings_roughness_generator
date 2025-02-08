import os
import processing
import pandas as pd
from qgis.core import (
    QgsProcessing,
    QgsApplication,
    QgsProcessingException,
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
        self.parameters = parameters
        self.context = context
        self.feedback = feedback
        self.outputs = {}
        self.results = {}
        self.lookup_folder = os.path.join(os.path.dirname(__file__), "lookups")
        self.landcover_vrt = os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt")

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

        # Step 2: Clip ESA Land Cover Raster to AOI
        clipped_landcover = clipRasterByExtent(
            self.landcover_vrt, extent, self.parameters["ManningRoughness"], self.context, self.feedback
        )
        
        # Step 3: Select the correct lookup file based on ROUGHNESS_CLASS
        roughness_lookup = ["low_n.csv", "med_n.csv", "high_n.csv"]
        selected_lookup = roughness_lookup[self.parameters["ROUGHNESS_CLASS"]]
        lookup_file = os.path.join(self.lookup_folder, selected_lookup)
        
        lookup_df = pd.read_csv(lookup_file)
        lookup_dict = dict(zip(lookup_df["lc"], lookup_df["n"]))

        exprs = " + ".join([f"(A=={lc})*{n}" for lc, n in lookup_dict.items()])

        # Step 4: Apply raster calculation to generate Manning roughness raster
        input_dict = {"input_a": clipped_landcover, "band_a": 1}
        roughness_raster = perform_raster_math(
            exprs, input_dict, self.context, self.feedback, no_data=-9999, out_data_type=5,
            output=self.parameters["ManningRoughness"]
        )

        # Step 5: Polygonize (optional)
        if self.parameters.get("ManningRoughnessVector"):
            self.outputs["ManningRoughnessVector"] = gdalPolygonize(
                roughness_raster, "roughness", self.parameters["ManningRoughnessVector"], self.context, self.feedback
            )
            apply_style(self.outputs["ManningRoughnessVector"], "manning_roughness_vector.qml", self.context)
            self.results["ManningRoughnessVector"] = self.outputs["ManningRoughnessVector"]

        # Step 6: Apply style and return results
        apply_style(roughness_raster, "manning_roughness_raster.qml", self.context)
        self.results["ManningRoughness"] = roughness_raster

        return self.results
