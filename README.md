# manning_roughness_generator
A QGIS plugin to generate the 2D Manning's Roughness dataset. 


Manning Roughness Generator
Overview

Manning Roughness Generator is a QGIS plugin designed to compute Manning's roughness coefficients from land cover datasets, particularly ESA WorldCover data. This tool is useful for hydrological and hydraulic modeling applications.
Features

    Clips ESA WorldCover land cover raster to an Area of Interest (AOI)

    Computes Manning's roughness coefficients based on user-defined roughness classes

    Supports raster and vector output

    Applies pre-defined QGIS styles to generated outputs

Installation

    Copy the plugin folder into the QGIS plugin directory:
    ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/

    Restart QGIS and activate the plugin from the Plugin Manager.

Usage

    Open QGIS and navigate to Processing Toolbox.

    Search for Manning Roughness Generator.

    Configure the input parameters:

        Area of Interest (AOI): Select a polygon layer defining the area of interest.

        Roughness Class: Choose from Low, Medium, or High.

        Output Raster: Path to save the generated Manning roughness raster.

        Output Vector (Optional): Path to save the polygonized version of the roughness raster.

    Click Run to generate the Manning roughness layer.

Input Data

    ESA WorldCover 2021 (esa_worldcover_2021.vrt)

    Lookup Tables (lookups/low_n.csv, lookups/med_n.csv, lookups/high_n.csv)

Output Data

    Manning Roughness Raster (GeoTIFF)

    Manning Roughness Vector (Optional, Polygon Shapefile)

    Styled Outputs (Using .qml style files)

Plugin Structure
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
Example Workflow

    Select an AOI (e.g., a watershed boundary).

    Run the Manning Roughness Generator with the desired roughness class.

    Retrieve the generated roughness raster and optionally vectorize it.

    Apply styling for visualization in QGIS.

Contact

Author: Abdullah Azzam
Email: mabdazzam@outlook.com
GitHub: Manning Roughness Plugin
License

This plugin is released under the MIT License.
