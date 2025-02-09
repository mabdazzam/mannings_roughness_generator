from qgis.core import QgsProcessingProvider, QgsApplication
from qgis.PyQt.QtGui import QIcon

import os
import inspect
import sys



from .manning_roughness_algorithm import ManningRoughnessAlgorithm

class ManningRoughnessProvider(QgsProcessingProvider):
    def __init__(self):
        """
        Default constructor.
        """
        super().__init__()

    def loadAlgorithms(self):
        """Load the processing algorithms"""
        self.addAlgorithm(ManningRoughnessAlgorithm())

    def id(self):
        return "manningroughness"

    def name(self):
        return self.tr("Manning Roughness")

    def icon(self):
        """Return provider icon"""
        return QIcon(os.path.join(os.path.dirname(__file__), "icon.png"))

    def initGui(self):
        """Initialize GUI elements if necessary"""
        pass  # makes sure  QGIS doesn't fail due to missing GUI setup

    def unload(self):
        """Unload provider from QGIS Processing framework"""
        QgsApplication.processingRegistry().removeProvider(self)

