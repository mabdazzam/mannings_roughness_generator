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
from qgis.core import QgsProcessingProvider, QgsApplication
from qgis.PyQt.QtGui import QIcon

from .mannings_roughness_algorithm import ManningsRoughnessAlgorithm

class ManningsRoughnessProvider(QgsProcessingProvider):
    def __init__(self):
        """
        Default constructor.
        """
        super().__init__()

    def loadAlgorithms(self):
        """Load the processing algorithms"""
        self.addAlgorithm(ManningsRoughnessAlgorithm())

    def id(self):
        return "manningsroughness"

    def name(self):
        return self.tr("Manning's Roughness Generator")

    def icon(self):
        """Return provider icon"""
        return QIcon(os.path.normpath(os.path.join(os.path.dirname(__file__), "icon.png")))

    def initGui(self):
        """Initialize GUI elements if necessary"""
        pass  # makes sure QGIS doesn't fail due to missing GUI setup

    def unload(self):
        """Unload provider from QGIS Processing framework"""
        QgsApplication.processingRegistry().removeProvider(self)

