# Manning's Roughness Generator
## Overview

Manning Roughness Generator is a QGIS plugin designed to compute Manning's
roughness coefficients from land cover datasets, particularly ESA WorldCover
data. This tool is useful for hydrological and hydraulic modeling applications.

## Features

1. Clips ESA WorldCover land cover raster to an Area of Interest (AOI)
2. Computes Manning's roughness coefficients based on user-defined roughness classes
3. Generates the roughness raster for low, medium, and high roughness conditions. 

## Installation

Download the zip and:

1. Install the zipped plugin;

        Open QGIS
        Manage and Install Plugins
        Install from ZIP
        Browse and Select ZIP
        OK.
   
2. Extract and copy the plugin folder into the QGIS plugin directory;

  For Linux;

    ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/

  For Windows;

     %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\

You can also access the plugins directory from;

      Settings
      User Profiles
      Open Active Profile Folder
      default/python/plugins
      
3. Restart QGIS and activate the plugin from the Plugin Manager.

## Usage

Open QGIS and navigate to Processing Toolbox.

Search for Manning Roughness Generator.

Configure the input parameters:

    1. Area of Interest (AOI): Select a polygon layer defining the area of
    interest.
    
    2. Roughness Class: Choose from Low, Medium, or High.

    3. Output Raster: Path to save the generated Manning roughness raster.

    4. Click Run to generate the Manning roughness layer.

## Input Data

1. Vector Area of Interest [Required]
2. ESA WorldCover 2021 (esa_worldcover_2021.vrt) [Provided]
3. Lookup Tables (lookups/low_n.csv, lookups/med_n.csv, lookups/high_n.csv) [Provided]

## Output Data

1. Manning Roughness Raster (GeoTIFF)
2. ESA Worldcover 2021 for the AOI.

## Contact

[Outlook](mabdazzam@outlook.com)

## License

This plugin is released under the GNU General Public License 3.0.
