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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .mannings_roughness_algorithm import ManningsRoughnessAlgorithm

class ManningsRoughnessProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        """Load the processing algorithms"""
        self.addAlgorithm(ManningsRoughnessAlgorithm())
    
    def id(self):
        return "manningsroughness"
    
    def name(self):
        return self.tr("Manning's Roughness")
    
    def icon(self):
        return QIcon("icon.png")

def classFactory(iface):
    """Load the provider into QGIS"""
    return ManningsRoughnessProvider()
