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
#class ManningRoughnessCalculator:
#    def __init__(self, parameters, context, feedback):
#        self.parameters = parameters
#        self.context = context
#        self.feedback = feedback
#        self.outputs = {}
#        self.results = {}
#        self.lookup_folder = os.path.join(os.path.dirname(__file__), "lookups")
#        # Define the path to the ESA WorldCover VRT file
#        self.landcover_vrt = os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt")
#        self.lc_pixel_size = 0.000083333333333


class ManningRoughnessCalculator:
    def __init__(self, parameters, context, feedback, esa_raster, lookup_table, output_raster, output_vector):
        self.parameters = parameters
        self.context = context
        self.feedback = feedback
        self.esa_raster = esa_raster
        self.lookup_table = lookup_table
        self.output_raster = output_raster
        self.output_vector = output_vector

        self.outputs = {}
        self.results = {}

        feedback.pushInfo(f"ESA raster received in calculator: {self.esa_raster}")

        if not os.path.exists(self.esa_raster):
            raise QgsProcessingException(f"ESA raster missing inside calculator: {self.esa_raster}")

def classFactory(iface):
    """Load the Manning Roughness Generator plugin"""
    provider = ManningRoughnessProvider()
    QgsApplication.processingRegistry().addProvider(provider)
    return provider


