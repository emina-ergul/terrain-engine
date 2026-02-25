# Project Overview

This project uses an SRTM GL1 30 dataset in GeoTiff format of DEM data (Digital Elevation Model) of a small area in Brecon, Wales to calculate the slope, aspect, hillshade, and curvature of the terrain. With the help of matplotlib, the frontend displays a visual of the terrain analysis outcome.

# terrain-engine learning points

### General

- In a **DEM** (digital elevation model) each pixel is an elevation value

- A .tiff (GeoTiff) is **raster data**, which is a grid of pixels and each pixel stores a value

- GeoJSON is vector not raster data

- Using EPSG:27700 (British National Grid) means the units are in meters

- To calculate just the pixel grid data, you can use src.read(1) to receive the raw pixels as a numpy array.

- The **profile** contains geo metadata

- Saving with profile reinserts the geo metadata after calculations have been made so that the raster remians georeferenced

- When opening a file with rasterio, src.res returns 2 values (dx, dy), one for pixel width and one for pixel height

- Mounting the PNGs in FastAPI was a good flexible way to bridge between the backend and frontend, allowign the browser to access the images at a fastAPI url

- cache bit

### Calculating slope (steepness)

- np.gradient() computes the chnage in elevation between pixels (dx dy)

- sqrt() is used to calculate gradient magnitude

-arctan() is used to get the rise/run and converts to an angle: rise run being the slope bc slope = rise/run e.g is rise is 10m and run is 20m, 10/20 = 0.5

- degrees() converts the result from radians

### Calculating aspect (which direction a hill is facing)

- arctan2 is used to calculate which direction the slope is facing using the slope results already calculated. kinda acts like a compass

- As aspect needs to be between 0 and 360 liek a compass,  (aspect + 360) % 360 ensures negative values are made positive (already pos values remain the same here)

### Calculating hillshade




### Calculating curvature

- involves calcuklating the gradient of a gradient of slope in both E-W directions and then N-S, e.g first gradient calc works out the slope along x and second gradient calc works out how the slope change i.e bends. this was probably the most difficult bit for me to understand

- the axis arg is used in np.gradient here to indicate moving up down (axis=0) and moving across (axis=1)

- adding the curavture values for E-W and N-S togther gives total surface curving. Positive would indicate convex and negative value would mean concave

- Initially my curvature data was producing a blank grey plot in matplotlib which made me believe the curvature calculations were wrong, because when printing them, np returned a big array of zeros. However, using np.nanmin and np.nanmax I could see the min and max values were infact not zero. After some investigating, it turns out numpy can have formatting issues when printing large arrays and can round numbers down to simplify. However my map was still grey. I think this meant almost all of the curvature values were very close to zero, and only a few where more extreme, making the visual practically one colour. To adjust this for the sake of the visual, I had to scale the values. Using np.nanpercentile I could remove the extreme values i.e np.nanpercentile(data, 5) to get the minimum value where 5% of values are lower, and the same for np.nanpercentile(data, 95) to get the max where 95% of values are lower, essentially cutting out the extremes

### Resources

<https://portal.opentopography.org/datasets>
<https://matplotlib.org/stable/users/index.html>
<https://earthdatascience.org/tutorials/get-slope-aspect-from-digital-elevation-model/>
<https://vuejs.org/guide/typescript/overview.html>
