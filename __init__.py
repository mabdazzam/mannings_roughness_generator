from qgis.core import QgsApplication
from .provider import ManningRoughnessProvider

def classFactory(iface):
    """Load the Manning Roughness Generator plugin"""
    provider = ManningRoughnessProvider()
    QgsApplication.processingRegistry().addProvider(provider)
    return provider 
