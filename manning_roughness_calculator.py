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

from qgis.core import QgsProcessingException, QgsProcessingUtils, QgsVectorLayer
from .utils import (
        clipRasterByExtent,
        perform_raster_math,
        load_manning_lookup,
        gdalPolygonize,
        apply_style,
        )

class ManningRoughnessCalculator:
    def __init__(self, parameters, context, feedback, esa_raster, lookup_table, output_raster, output_vector):
        """
        Initializes the Manning Roughness Calculator.

        :param parameters: QGIS processing parameters
        :param context: QGIS processing context
        :param feedback: QGIS feedback object for logging
        :param esa_raster: The preprocessed ESA raster to be used for roughness calculation
        :param lookup_table: The lookup table containing Manning roughness values
        :param output_raster: The destination path for the Manning Roughness raster
        :param output_vector: The optional destination path for the vectorized roughness layer
        """
        self.parameters = parameters
        self.context = context
        self.feedback = feedback
        self.esa_raster = esa_raster  # 
        self.lookup_table = lookup_table  
        self.output_raster = output_raster 
        self.output_vector = output_vector  

        self.outputs = {}
        self.results = {}


    def run(self):
        """Performs the Manning Roughness calculation using ESA Land Cover and lookup table."""
        self.feedback.pushInfo("Starting Manning Roughness calculation...")

        # Step 1: ensure ESA raster exists
        self.esa_raster = os.path.normpath(self.esa_raster) ## normalized path for windows
        if not os.path.exists(self.esa_raster):
            raise QgsProcessingException(f"ESA raster is missing: {self.esa_raster}")

        self.feedback.pushInfo(f"Using ESA raster: {self.esa_raster} for roughness computation.")

        # Step 2: load lookup table based on user selection
        roughness_lookup = ["low_n.csv", "med_n.csv", "high_n.csv"]
        selected_lookup = roughness_lookup[self.parameters["ROUGHNESS_CLASS"]]
        #lookup_file = os.path.join(os.path.dirname(__file__), "lookups", selected_lookup)
        lookup_file = os.path.normpath(os.path.join(os.path.dirname(__file__), "lookups", selected_lookup)) ## normalized path for windows

        self.feedback.pushInfo(f"Loading Manning Roughness lookup table from: {lookup_file}")

        if not os.path.exists(lookup_file):
            raise QgsProcessingException(f"Lookup table not found: {lookup_file}")

        # Step 3: read lookup CSV dile
        lookup_values = []
        #with open(lookup_file, "r") as file:
        with open(lookup_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip header
                parts = line.strip().split(",")
                if len(parts) == 2:
                    try:
                        lc_value = int(parts[0])  
                        n_value = float(parts[1])
                        lookup_values.append((lc_value, n_value))
                    except ValueError:
                        self.feedback.pushWarning(f"Skipping invalid row in lookup file: {line.strip()}")

                        if not lookup_values:
                            raise QgsProcessingException(f"Lookup table {selected_lookup} is empty or malformed.")

        self.feedback.pushInfo(f"Loaded {len(lookup_values)} land cover to roughness mappings.")

        # Step 4: generate raster calculation expression
        exprs = " + ".join([f"(A == {lc}) * {n}" for lc, n in lookup_values])
        self.feedback.pushInfo(f"Generated raster math expression: {exprs}")

        # Step 5:  perform raster calculation to assign manning roughness values
        input_dict = {"input_a": self.esa_raster, "band_a": 1}
        self.outputs["ManningRoughness"] = perform_raster_math(
                exprs, input_dict, self.context, self.feedback, no_data=-9999, out_data_type=5,
                output=self.output_raster
                )

        if not os.path.exists(self.outputs["ManningRoughness"]):
            raise QgsProcessingException("Manning Roughness raster was not created!")

        self.feedback.pushInfo(f"Manning Roughness raster saved at: {self.outputs['ManningRoughness']}")

        ## in the following step (VectorRoughness) gdal polygonize does not seem to work (even manually)
        # review of vectorization methods and usage of the appropirate one is required. 

        # Step 6: vectorize the raster if required
        if self.output_vector:
            # Use the exact raster produced in Step 5
            self.outputs["ManningRoughnessVector"] = gdalPolygonize(
                    self.outputs["ManningRoughness"], 
                    "n",  
                    output=self.output_vector,
                    context=self.context,
                    feedback=self.feedback,
                    )

            if not os.path.exists(self.outputs["ManningRoughnessVector"]):
                raise QgsProcessingException("Manning Roughness vectorization failed!")

            self.feedback.pushInfo(f"Manning Roughness Vector saved at: {self.outputs['ManningRoughnessVector']}")

        return {"ManningRoughness": self.outputs["ManningRoughness"]}
