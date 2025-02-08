### Manning Roughness Generator
## Overview

Manning Roughness Generator is a QGIS plugin designed to compute Manning's roughness coefficients from land cover datasets, particularly ESA WorldCover data. This tool is useful for hydrological and hydraulic modeling applications.
## Features

1. Clips ESA WorldCover land cover raster to an Area of Interest (AOI)

2. Computes Manning's roughness coefficients based on user-defined roughness classes

3. Supports raster and vector output

4. Generates the low, medium, and high roughness conditions. 

## Installation

Copy the plugin folder into the QGIS plugin directory:

    ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/

Restart QGIS and activate the plugin from the Plugin Manager.

## Usage

Open QGIS and navigate to Processing Toolbox.

Search for Manning Roughness Generator.

Configure the input parameters:

        Area of Interest (AOI): Select a polygon layer defining the area of interest.

        Roughness Class: Choose from Low, Medium, or High.

        Output Raster: Path to save the generated Manning roughness raster.

        Output Vector (Optional): Path to save the polygonized version of the roughness raster.

    Click Run to generate the Manning roughness layer.

## Input Data

ESA WorldCover 2021 (esa_worldcover_2021.vrt) [Provided]

Lookup Tables (lookups/low_n.csv, lookups/med_n.csv, lookups/high_n.csv) [Provided]

Vector Area of Interest [Required by the user]

## Output Data

Manning Roughness Raster (GeoTIFF)

Manning Roughness Vector (Optional, Polygon Shapefile)

ESA Worldcover 2021 for the AOI.

## Plugin Structure
Manning_Roughness_Generator/
├── __init__.py                 # Registers the plugin in QGIS
├── metadata.txt                # Plugin metadata
├── provider.py                 # Processing provider for QGIS
├── manning_roughness_generator.py # Main plugin entry
├── manning_roughness_algorithm.py # Processing algorithm
├── manning_roughness_calculator.py # Main calculation logic
├── utils.py                     # Utility functions
├── esa_worldcover_2021.vrt       # Reference land cover dataset
├── manning_roughness_raster.qml  # Style file for raster output
├── manning_roughness_vector.qml  # Style file for vector output
└── lookups/                      # Lookup tables for roughness coefficients


## Contact

Author: Abdullah Azzam
Email: mabdazzam@outlook.com
GitHub: Manning Roughness Plugin

## License

This plugin is released under the MIT License.



