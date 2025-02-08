import os
import pickle
import time
import xml.etree.ElementTree as ET
import csv

import processing
import requests
from qgis.core import (
    Qgis,
    QgsRasterLayer
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsCoordinateTransformContext,
    QgsDistanceArea,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingException,
    QgsProject,
    QgsVectorLayer,
)
from qgis.PyQt.QtWidgets import QPushButton
from qgis.utils import iface

def fetchMessage(url, timeout=2) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text

def saveToCache(message, cache_path):
    with open(cache_path, "w") as file:
        file.write(message)

def isCacheValid(cache_path, duration):
    if os.path.exists(cache_path):
        file_timestamp = os.path.getmtime(cache_path)
        if time.time() - file_timestamp < duration:
            return True
    return False

def loadMessageFromCache(cache_path):
    if isCacheValid(cache_path, 24 * 60 * 60):
        with open(cache_path, "r") as file:
            return file.read()
    return ""

def apply_style(layer_path, style_path, context):
    """Apply QGIS layer style (.qml)"""
    layer = QgsRasterLayer(layer_path, "Manning Roughness Layer", "gdal")  # Explicitly load raster
    if layer.isValid() and style_path and os.path.exists(style_path):
        layer.loadNamedStyle(style_path)
        layer.triggerRepaint()
    else:
        print(f"Failed to apply style: Invalid layer or missing style file {style_path}")

def clipRasterByExtent(input_raster, extent, output_path, context, feedback):
    """Clip a raster using a bounding box extent"""
    clip_params = {
        "DATA_TYPE": 0,
        "INPUT": input_raster,
        "NODATA": None,
        "OPTIONS": "",
        "EXTRA": "",
        "PROJWIN": f"{extent.xMinimum()},{extent.xMaximum()},{extent.yMinimum()},{extent.yMaximum()} [EPSG:4326]",
        "OUTPUT": output_path,
    }
    return processing.run("gdal:cliprasterbyextent", clip_params, context=context, feedback=feedback)["OUTPUT"]

def generate_manning_exprs(lookup_table_path, nodata=-9999):
    """Generate raster math expression for Manning roughness"""
    exprs = []
    with open(lookup_table_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            land_cover_code, roughness = row
            exprs.append(f"(A == {land_cover_code}) * {roughness}")
    return f" + ".join(exprs) if exprs else str(nodata)

def perform_raster_math(exprs, input_dict, context, feedback, no_data, out_data_type, output=QgsProcessing.TEMPORARY_OUTPUT):
    alg_params = {
        "FORMULA": exprs,
        "INPUT_A": input_dict.get("input_a"),
        "BAND_A": input_dict.get("band_a"),
        "NO_DATA": no_data,
        "RTYPE": out_data_type,
        "OUTPUT": output,
    }
    return processing.run("gdal:rastercalculator", alg_params, context=context, feedback=feedback, is_child_algorithm=True)["OUTPUT"]

def gdalPolygonize(input, field="value", output=QgsProcessing.TEMPORARY_OUTPUT, context=None, feedback=None):
    params = {"INPUT": input, "FIELD": field, "OUTPUT": output}
    return processing.run("gdal:polygonize", params, context=context, feedback=feedback, is_child_algorithm=True)["OUTPUT"]

def downloadFile(request_URL, context=None, feedback=None):
    try:
        alg_params = {"URL": request_URL, "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT}
        return processing.run("native:filedownloader", alg_params, context=context, feedback=feedback, is_child_algorithm=True)["OUTPUT"]
    except (QgsProcessingException, requests.exceptions.HTTPError) as e:
        feedback.reportError(f"Error: {str(e)}")
