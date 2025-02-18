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
import sys
import inspect
import processing

from qgis.core import QgsApplication
from .provider import ManningsRoughnessProvider

class ManningsRoughnessCalculator:
    def __init__(self, parameters, context, feedback, esa_raster, lookup_table, output_raster):
        self.parameters = parameters
        self.context = context
        self.feedback = feedback
        self.lookup_folder = os.path.normpath(os.path.join(os.path.dirname(__file__), "lookups"))
        self.landcover_vrt = os.path.normpath(os.path.join(os.path.dirname(__file__), "esa_worldcover_2021.vrt"))
        self.esa_raster = os.path.normpath(esa_raster)
        self.lookup_table = os.path.normpath(lookup_table)
        self.output_raster = os.path.normpath(output_raster)

        self.outputs = {}
        self.results = {}

        feedback.pushInfo(f"ESA raster received in calculator: {self.esa_raster}")

        # Check if ESA raster exists
        if not os.path.exists(self.esa_raster):
            raise QgsProcessingException(f"ESA raster missing inside calculator: {self.esa_raster}")

def saveToCache(message, cache_path):
    """Save a message to a file"""
    cache_path = os.path.normpath(cache_path)  # Ensure correct path format
    with open(cache_path, "w") as file:
        file.write(message)

def classFactory(iface):
    """Load the Manning's Roughness Generator plugin"""
    provider = ManningsRoughnessProvider()
    QgsApplication.processingRegistry().addProvider(provider)
    return provider

