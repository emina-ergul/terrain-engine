# Project overview

This project uses an SRTM GL1 30 dataset in GeoTiff format of a small area in Brecon, Wales to calculate the slope, aspect, hillshade, and curvature of the terrain.

# terrain-engine learning points

A .tiff (GeoTiff) is raster data, which is a grid of pixels and each pixel stores a value

GeoJSON is vector not raster data

A DEM (digital elevation) each pixel is an elevation value

Each pixel may also have slope in degrees and hillshade in brightness. It also containes other info like location on earth, pixel size, and projection

The profile contains geo metadata

To calculate just the pixel grid data, you can use src.read(1). Saving with profile reinserts the geo metadata after calculations have been made
