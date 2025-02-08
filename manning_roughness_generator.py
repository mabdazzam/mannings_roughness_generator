from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from .manning_roughness_algorithm import ManningRoughnessAlgorithm

class ManningRoughnessProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        """Load the processing algorithms"""
        self.addAlgorithm(ManningRoughnessAlgorithm())
    
    def id(self):
        return "manningroughness"
    
    def name(self):
        return self.tr("Manning Roughness")
    
    def icon(self):
        return QIcon("icon.png")

def classFactory(iface):
    """Load the provider into QGIS"""
    return ManningRoughnessProvider()
