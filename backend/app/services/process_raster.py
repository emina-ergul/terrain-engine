import os
import numpy as np
import rasterio

processed_dir = "./storage/processed"


def clear_old_processed_files():
    if os.path.exists(processed_dir):
        for file in os.listdir(processed_dir):
            os.remove(os.path.join(processed_dir, file))


# slope, gradient caluclates the chnage in elevation between x and y
def calculate_slope(dem, dx, dy):
    dz_dy, dz_dx = np.gradient(dem, abs(dy), dx)
    slope = np.degrees(np.arctan(np.sqrt(dz_dx**2 + dz_dy**2)))
    return slope, dz_dx, dz_dy


# aspect is direction of slope
def calculate_aspect(dz_dx, dz_dy):
    aspect = np.degrees(np.arctan2(dz_dx, -dz_dy))
    aspect = (aspect + 360) % 360
    return aspect


# hillshade is sunlight and shadow
def calculate_hillshade(slope, aspect):
    sun_azimuth = 315  # NW direction
    sun_altitude = 45  # 45 degree above horizon
    az_rad = np.radians(sun_azimuth)
    alt_rad = np.radians(sun_altitude)

    hs = np.sin(alt_rad) * np.cos(np.radians(slope)) + np.cos(alt_rad) * np.sin(
        np.radians(slope)
    ) * np.cos(az_rad - np.radians(aspect))
    hillshade = np.clip(hs * 255, 0, 255)
    return hillshade


# curvature is the surface bending (+ is convex, - is concave)
def calculate_curvature(dem, dx, dy):
    dxx = np.gradient(np.gradient(dem, dx, axis=1), dx, axis=1)
    dyy = np.gradient(np.gradient(dem, dy, axis=0), dy, axis=0)
    curvature = dxx + dyy

    print("Curvature min/max:", np.nanmin(curvature), np.nanmax(curvature))
    return curvature


def save_raster(profile, name, data):
    out_profile = profile.copy()
    out_profile.update(dtype=rasterio.float32, count=1)
    out_path = os.path.join(processed_dir, f"{name}.tiff")
    with rasterio.open(out_path, "w", **out_profile) as dst:
        dst.write(data.astype(rasterio.float32), 1)
        print(f"Saved {name} to {out_path}")


def process_terrain(tif_file):
    clear_old_processed_files()

    print("Starting terrain processing...")

    # Reprojected to EPSG:27700 using GDAL bc im using data of Brecon
    raw_data = f"./storage/raw/{tif_file}"
    os.makedirs(processed_dir, exist_ok=True)

    with rasterio.open(raw_data) as src:
        dem = src.read(1)
        profile = src.profile
        dx, dy = src.res

    slope, dz_dx, dz_dy = calculate_slope(dem, dx, dy)

    aspect = calculate_aspect(dz_dx, dz_dy)

    hillshade = calculate_hillshade(slope, aspect)

    curvature = calculate_curvature(dem, dx, dy)

    for name, data in [
        ("slope", slope),
        ("aspect", aspect),
        ("hillshade", hillshade),
        ("curvature", curvature),
    ]:
        save_raster(profile, name, data)

    print("Processing complete!!!")
