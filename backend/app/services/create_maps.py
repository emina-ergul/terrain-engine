import rasterio
import matplotlib
import time

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os


def remove_maps():
    maps_dir = "./storage/maps"
    if os.path.exists(maps_dir):
        for file in os.listdir(maps_dir):
            os.remove(os.path.join(maps_dir, file))


def create_maps():
    remove_maps()
    processed_dir = "./storage/processed"
    tiffs = os.listdir(processed_dir)

    for name in tiffs:
        path = os.path.join(processed_dir, name)
        with rasterio.open(path) as src:
            data = src.read(1)
            nodata = src.nodata
            data = np.where(data == nodata, np.nan, data)

        plt.figure(figsize=(6, 6))

        vmin = None
        vmax = None

        if "hillshade" in name:
            cmap = "gray"
        elif "slope" in name:
            cmap = "terrain"
        elif "aspect" in name:
            cmap = "hsv"
        elif "curvature" in name:
            cmap = "RdBu"
            vmin = np.nanpercentile(data, 5)
            vmax = np.nanpercentile(data, 95)
        print("!!!!!!!!!!!!!!!!!!!!!!!!")
        plt.figure(figsize=(6, 6))
        im = plt.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)
        plt.title(name.split(".")[0].capitalize())
        plt.axis("off")
        plt.colorbar(im)

        output_dir = "./storage/maps"
        os.makedirs(output_dir, exist_ok=True)
        output_img_path = os.path.join(output_dir, f"{name.split('.')[0]}.png")
        plt.savefig(output_img_path)
        plt.close()
        print(f"Saved {name} map to {output_img_path}")
