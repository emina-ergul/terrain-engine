# Project Overview

This project uses a GeoTiff of SRTM GL1 30 dataset of DEM data (Digital Elevation Model) to calculate the slope, aspect, hillshade, and curvature of the terrain. With the help of matplotlib, the frontend displays a visual of the terrain analysis outcome.

# To run

After cloning the repo, you'll need to have installed anaconda or miniconda to replicate the env from your terminal with:

- conda env create -f environment.yaml
- conda activate terrain-engine-env

Go into the backend folder and run 'just run'

Go into the frontend folder and run 'npm run dev'

# Screenshots
Initial page
<img width="1918" height="455" alt="Initial page of terrain engine" src="https://github.com/user-attachments/assets/ed1334b4-0a9c-4f57-ab3b-2493fae1e6c2" />
<br>
<br>
Generated maps example
<img width="1912" height="990" alt="Example of generated terrain attribute maps" src="https://github.com/user-attachments/assets/aa40fc35-2ac5-4412-83b9-f36be42c7297" />

# terrain-engine learning points

### Data

- A **DEM** (digital elevation model) is a map of elevation, where data is like a grid and each plot represents an area of certain size

- **raster data** is a grid of pixels and each pixel stores a numerical value

- A GeoTiff is a raster file format that holds the grid data but with additional geographical metadata like georeferencing so the location on earth is known

- GeoJSON is vector not raster data

- EPSG is a code used to define geospatial referncing, ensuring consistent spatial referencing across different software. Codes can be used in transforming coordinate data from lat/long to UTM for example.

- EPSG:27700 (British National Grid) is a CRS for Great Britain with the units in meters

- In order to dynamically adjust for any ESPG code (because some use degrees and not meters), I converted to UTM(universal tranverse mercator) using gdal.Warp() if the data is in degrees, which creates a new raster file with projected CRS(coordinate refernece system)

- To get the pixel grid data, you can use src.read(1) to receive the raw pixels as a numpy array.

- The rasterio **profile** contains the geo metadata

- Saving with profile reinserts the geo metadata after calculations have been made so that the raster remains georeferenced

- When opening a file with rasterio, src.res returns 2 values (dx, dy), one for pixel width and one for pixel height, these are the spacing values


### General

- Mounting the PNGs in FastAPI was a good flexible way to bridge between the backend and frontend, allowign the browser to access the images at a fastAPI url


### Calculating slope (steepness)

- np.gradient() computes the chnage in elevation between pixels (dx dy)

- sqrt() is used to calculate gradient magnitude

- arctan() is used to get the rise/run and converts to an angle: rise run being the slope bc slope = rise/run e.g is rise is 10m and run is 20m, 10/20 = 0.5

- degrees() converts the result from radians


### Calculating aspect (which direction a hill is facing)

- arctan2 is used to calculate which direction the slope is facing using the slope results already calculated. kinda acts like a compass

- As aspect needs to be between 0 and 360 liek a compass,  (aspect + 360) % 360 ensures negative values are made positive (already pos values remain the same here)

### Calculating hillshade


- First an altitude and azimuth (compass direction of sun) for the sun needs to be picked in degrees. These values then get converted to radians using np.radians()

- The use of the trigonometry calculations here were definitely the most difficult part for me to understand so I tried to simplify it for my understanding. Basically this is to find total brightness by adding light from above to light from sideways.

- I was able to deduce that the direction of the sunlight was acting as the hypotenuse

- Then it can be thought of as each point of light in the set direction being cut both vertically (sine) and horizontally (cosine)

- The calculations essentially represent:
     
     (vertical light * vertical surface response) + (horizontal light * horizontal surface response * direction match)


- np.clip() turns it into a grayscale by 'clipping' the array, multiplying by 255 turns it into a brightness scale between 0 and 255


### Calculating curvature

- involves calcuklating the gradient of a gradient of slope in both E-W directions and then N-S, e.g first gradient calc works out the slope along x and second gradient calc works out how the slope change i.e bends.

- the axis arg is used in np.gradient here to indicate moving up down (axis=0) and moving across (axis=1)

- adding the curavture values for E-W and N-S togther gives total surface curving. Positive would indicate convex and negative value would mean concave

- Initially my curvature data was producing a blank grey plot in matplotlib which made me believe the curvature calculations were wrong, because when printing them, np returned a big array of zeros. However, using np.nanmin and np.nanmax I could see the min and max values were infact not zero. After some investigating, it turns out numpy can have formatting issues when printing large arrays and can round numbers down to simplify. However my map was still grey. I think this meant almost all of the curvature values were very close to zero, and only a few where more extreme, making the visual practically one colour. To adjust this for the sake of the visual, I had to scale the values. Using np.nanpercentile I could remove the extreme values i.e np.nanpercentile(data, 5) to get the minimum value where 5% of values are lower, and the same for np.nanpercentile(data, 95) to get the max where 95% of values are lower, essentially cutting out the extremes

### Resources

- <https://portal.opentopography.org/datasets>
- <https://en.wikipedia.org/wiki/Digital_elevation_model>
- <https://rasterio.readthedocs.io/en/stable/topics/reading.html>
- <https://earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/fundamentals-raster-data/raster-metadata-in-python/>
- <https://matplotlib.org/stable/users/index.html>
- <https://earthdatascience.org/tutorials/get-slope-aspect-from-digital-elevation-model/>
- <https://vuejs.org/guide/typescript/overview.html>
