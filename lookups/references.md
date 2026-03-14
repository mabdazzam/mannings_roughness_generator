Medium = (low + high) / 2.

| ESA code | ESA class | low | medium | high | reference |
|---|---|---:|---:|---:|---|
| 10 | Tree cover | 0.080 | 0.140 | 0.200 | HEC-RAS land classification ranges for forest classes: Evergreen Forest 0.08–0.16, Deciduous Forest 0.10–0.20, Mixed Forest 0.08–0.20. |
| 20 | Shrubland | 0.035 | 0.098 | 0.160 | Chow (1959) floodplains, brush classes, including scattered brush/heavy weeds through medium to dense brush in summer; reproduced in Appendix-I. |
| 30 | Grassland | 0.025 | 0.038 | 0.050 | Chow (1959) floodplains, pasture/no brush: short grass and high grass; reproduced in Appendix-I. |
| 40 | Cropland | 0.020 | 0.035 | 0.050 | Chow (1959) floodplains, cultivated areas: no crop, mature row crops, mature field crops; reproduced in Appendix-I. |
| 50 | Built-up | 0.030 | 0.115 | 0.200 | HEC-RAS land classification ranges for developed classes: Open Space 0.03–0.05, Low Intensity 0.06–0.12, Medium Intensity 0.08–0.16, High Intensity 0.12–0.20. |
| 60 | Bare / sparse vegetation | 0.023 | 0.027 | 0.030 | HEC-RAS land classification range for Barren Land: 0.023–0.030. |
| 70 | Snow and ice | 0.010 | 0.020 | 0.030 | HEC-RAS ice-covered rivers guidance: fresh/new ice 1–3 ft thick = 0.01–0.03. |
| 80 | Permanent water bodies | 0.025 | 0.038 | 0.050 | HEC-RAS land classification range for Open Water: 0.025–0.05. |
| 90 | Herbaceous wetland | 0.050 | 0.068 | 0.085 | HEC-RAS land classification range for Emergent Herbaceous Wetlands: 0.05–0.085. |
| 95 | Mangroves | 0.045 | 0.098 | 0.150 | HEC-RAS land classification range for Woody Wetlands, used here as the mangrove proxy: 0.045–0.15. |
| 100 | Moss and lichen | 0.040 | 0.060 | 0.080 | Chow (1959) floodplains, brush: light brush and trees, in summer = 0.040, 0.060, 0.080; used here as the moss/lichen proxy. |

Full references

1. ESA WorldCover 10 m v100. Google Earth Engine Data Catalog. Official class order used here: 10 Tree cover, 20 Shrubland, 30 Grassland, 40 Cropland, 50 Built-up, 60 Bare / sparse vegetation, 70 Snow and ice, 80 Permanent water bodies, 90 Herbaceous wetland, 95 Mangroves, 100 Moss and lichen.
   https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100

2. U.S. Army Corps of Engineers Hydrologic Engineering Center. Land Classification Layers. HEC-RAS documentation. Used here for the ranges for forest, developed land, barren land, open water, herbaceous wetlands, and woody wetlands.
   https://www.hec.usace.army.mil/confluence/rasdocs/rmum/latest/land-classification-layers

3. U.S. Army Corps of Engineers Hydrologic Engineering Center. Modeling Ice Covers with Known Geometry. HEC-RAS 1D Technical Reference documentation. Used here for the snow/ice proxy range of 0.01–0.03 for fresh/new ice 1–3 ft thick.
   https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.5/modeling-ice-covered-rivers/modeling-ice-covers-with-known-geometry

4. Chow, V. T. (1959). Open-Channel Hydraulics. New York: McGraw-Hill. Floodplain Manning’s n values used here through the reproduced table in Appendix-I Surface Roughness and Manning’s “n” Table. Used here for shrubland, grassland, cropland, and the moss/lichen proxy.
   https://www.un-spider.org/sites/default/files/Table_Surface_roughness_Manning_n_Chow_1959.pdf
