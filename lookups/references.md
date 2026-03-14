# ESA Manning's n lookup table

| ESA code | ESA class | low | medium | high | reference |
|---|---|---:|---:|---:|---|
| 10 | Tree cover | 0.070 | 0.094 | 0.124 | HEC-RAS Table 3-1 / Chow excerpts: floodways with heavy stands of timber and brush = 0.070 / 0.100 / 0.150; flood-plain trees include heavy timber below branches = 0.080 / 0.100 / 0.120 and flow into branches = 0.100 / 0.120 / 0.160. |
| 20 | Shrubland | 0.045 | 0.066 | 0.096 | HEC-RAS Table 3-1 / Chow excerpts: medium to dense brush, winter = 0.045 / 0.070 / 0.110; medium to dense brush, summer = 0.070 / 0.100 / 0.160. |
| 30 | Grassland | 0.028 | 0.033 | 0.043 | HEC-RAS Table 3-1 / Chow excerpts: pasture, short grass = 0.025 / 0.030 / 0.035; pasture, high grass = 0.030 / 0.035 / 0.050. |
| 40 | Cropland | 0.025 | 0.035 | 0.045 | HEC-RAS Table 3-1 / Chow excerpts: cultivated areas, mature row crops = 0.025 / 0.035 / 0.045 (exact match). |
| 50 | Built-up | 0.016 | 0.018 | 0.020 | HEC-RAS Table 3-1 constructed-surface proxy: excavated or dredged channels, earth, straight and uniform, clean recently completed = 0.016 / 0.018 / 0.020 (exact match). HEC-RAS Land Cover is used as a surrogate for Manning's n and can be overridden with user-defined classification polygons. |
| 60 | Bare / sparse vegetation | 0.010 | 0.0225 | 0.035 | NRCS Chapter 15, Table 15-1: smooth surface (concrete, asphalt, gravel, or bare soil) = 0.011; HEC-RAS Land Classification: Barren Land = 0.023-0.030; HEC-RAS Table 3-1: rock cuts, smooth and uniform = 0.025 / 0.035 / 0.040. |
| 70 | Snow and ice | 0.010 | 0.020 | 0.030 | HEC-RAS ice-covered rivers, Table 11-1: rippled ice = 0.01 to 0.03; frazil ice, new 1 to 3 ft thick = 0.01 to 0.03. |
| 80 | Permanent water bodies | 0.025 | 0.035 | 0.045 | HEC-RAS Land Classification: Open Water = 0.025-0.05; HEC-RAS Table 3-1 / Chow excerpts: clean, winding, some pools and shoals = 0.033 / 0.040 / 0.045. |
| 90 | Herbaceous wetland | 0.060 | 0.090 | 0.120 | HEC-RAS Land Classification: Emergent Herbaceous Wetlands = 0.05-0.085; USGS WSP 2339 Table 3 vegetation adjustment: very large vegetation = 0.050-0.100, with dense cattails explicitly listed. |
| 95 | Mangroves | 0.150 | 0.225 | 0.300 | HEC-RAS Land Classification: Woody Wetlands = 0.045-0.15 for the low end; USGS WSP 2339 flood-plain method supports much larger values for dense woody vegetation using equation 6, extreme vegetation adjustment n4 = 0.100-0.200, and meander factor m up to 1.30. |
| 100 | Moss and lichen | 0.040 | 0.060 | 0.080 | HEC-RAS Table 3-1 / Chow excerpts: light brush and trees, in summer = 0.040 / 0.060 / 0.080, used here as the official proxy. |

## Full references

1. ESA WorldCover 10 m v100, Google Earth Engine Data Catalog.
   Class order used here: 10 Tree cover, 20 Shrubland, 30 Grassland, 40 Cropland, 50 Built-up, 60 Bare / sparse vegetation, 70 Snow and ice, 80 Permanent water bodies, 90 Herbaceous wetland, 95 Mangroves, 100 Moss and lichen.
   https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100

2. U.S. Army Corps of Engineers Hydrologic Engineering Center. Land Classification Layers.
   Used here for Open Water, Developed classes, Barren Land, Deciduous/Evergreen/Mixed Forest, Shrub/Scrub, Grassland/Herbaceous, Woody Wetlands, Emergent Herbaceous Wetlands, and the note that land cover is used as a surrogate for Manning's n and can be overridden with classification polygons.
   https://www.hec.usace.army.mil/confluence/rasdocs/rmum/latest/land-classification-layers

3. U.S. Army Corps of Engineers Hydrologic Engineering Center. Hydraulic Reference Manual / Energy Loss Coefficients, Table 3-1 Manning's n Values.
   Used here for Chow-derived table excerpts including flood-plain grass, crops, brush, trees, built-up/constructed channel values, rock cuts, and channel proxies.
   https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.6/basic-data-requirements/geometric-data/energy-loss-coefficients

4. U.S. Army Corps of Engineers Hydrologic Engineering Center. Modeling Ice Covers with Known Geometry, Table 11-1 Suggested Range of Manning's n Values for Ice Covered Rivers.
   Used here for snow/ice proxies.
   https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.5/modeling-ice-covered-rivers/modeling-ice-covers-with-known-geometry

5. Arcement, G.J., Jr., and Schneider, V.R. (1989). Guide for Selecting Manning's Roughness Coefficients for Natural Channels and Flood Plains. U.S. Geological Survey Water-Supply Paper 2339.
   Used here for the official flood-plain composite method, equation 6, vegetation adjustment ranges in Table 3, dense cattails example, and support for high roughness in densely vegetated woody flood plains.
   https://pubs.usgs.gov/wsp/2339/report.pdf

6. USDA Natural Resources Conservation Service. Chapter 15 - Time of Concentration.
   Used here for Table 15-1, which lists smooth surface (concrete, asphalt, gravel, or bare soil) = 0.011.
   https://directives.nrcs.usda.gov/sites/default/files2/1720461053/Chapter%2015%20-%20Time%20of%20Concentration.pdf
