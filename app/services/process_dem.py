import os
import numpy as np
import rasterio


def calculate_terrain():
    # Reprojected to EPSG:27700 using GDAL bc im using data of Brecon
    raw_data = "./storage/raw/brecon_dem_27700.tif"
    processed_dir = "./storage/processed"
    os.makedirs(processed_dir, exist_ok=True)

    with rasterio.open(raw_data) as src:
        dem = src.read(1)
        profile = src.profile
        dx, dy = src.res

    # slope, gradient caluclates the chnage in elevation between x and y
    dz_dy, dz_dx = np.gradient(dem, abs(dy), dx)
    slope = np.degrees(np.arctan(np.sqrt(dz_dx**2 + dz_dy**2)))

    # aspect is direction of slope
    aspect = np.degrees(np.arctan2(dz_dx, -dz_dy))
    aspect = (aspect + 360) % 360

    valid_aspect = aspect[dem != src.nodata]
    print("Aspect Min:", valid_aspect.min())
    print("Aspect Max:", valid_aspect.max())

    # hillshade is sunlight and shadow
    sun_azimuth = 315  # NW direction
    sun_altitude = 45  # 45 degree above horizon
    az_rad = np.radians(sun_azimuth)
    alt_rad = np.radians(sun_altitude)

    hs = np.sin(alt_rad) * np.cos(np.radians(slope)) + np.cos(alt_rad) * np.sin(
        np.radians(slope)
    ) * np.cos(az_rad - np.radians(aspect))
    hillshade = np.clip(hs * 255, 0, 255)

    # curvature is the surface bending (+ is convex, - is concave)
    dxx = np.gradient(np.gradient(dem, dx, axis=1), dx, axis=1)
    dyy = np.gradient(np.gradient(dem, dy, axis=0), dy, axis=0)
    curvature = dxx + dyy

    print("Curvature min/max:", np.nanmin(curvature), np.nanmax(curvature))

    for name, date in [
        ("slope", slope),
        ("aspect", aspect),
        ("hillshade", hillshade),
        ("curvature", curvature),
    ]:
        out_profile = profile.copy()
        out_profile.update(dtype=rasterio.float32, count=1)
        out_path = os.path.join(processed_dir, f"brecon_{name}.tiff")
        with rasterio.open(out_path, "w", **out_profile) as dst:
            dst.write(date.astype(rasterio.float32), 1)
        print(f"Saved {name} to {out_path}")

    print("Processing complete!!!")
