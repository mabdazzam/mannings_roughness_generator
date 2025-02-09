from qgis.core import QgsApplication
from .provider import ManningRoughnessProvider

#class ManningRoughnessCalculator:
#    def __init__(self, parameters, context, feedback):
#        self.parameters = parameters
#        self.context = context
#        self.feedback = feedback
#        self.outputs = {}
#        self.results = {}
#        self.lookup_folder = os.path.join(os.path.dirname(__file__), "lookups")
#        self.landcover_vrt = os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt")  # maube this would fix AttributeError: 'ManningRoughnessCalculator' object has no attribute 'landcover_vrt'
#
class ManningRoughnessCalculator:
    def __init__(self, parameters, context, feedback):
        self.parameters = parameters
        self.context = context
        self.feedback = feedback
        self.outputs = {}
        self.results = {}
        self.lookup_folder = os.path.join(os.path.dirname(__file__), "lookups")
        # Define the path to the ESA WorldCover VRT file
        self.landcover_vrt = os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt")



def classFactory(iface):
    """Load the Manning Roughness Generator plugin"""
    provider = ManningRoughnessProvider()
    QgsApplication.processingRegistry().addProvider(provider)
    return provider


