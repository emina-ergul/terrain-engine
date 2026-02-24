import rasterio
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os


def create_maps():
    processed_dir = "./storage/processed"
    tiffs = [
        "brecon_aspect.tiff",
        "brecon_slope.tiff",
        "brecon_hillshade.tiff",
        "brecon_curvature.tiff",
    ]

    plt.figure(figsize=(12, 10))

    for i, name in enumerate(tiffs, 1):
        path = os.path.join(processed_dir, name)
        with rasterio.open(path) as src:
            data = src.read(1)
            nodata = src.nodata
            data = np.where(data == nodata, np.nan, data)

        plt.subplot(2, 2, i)

        vmin = None
        vmax = None

        if name == "brecon_hillshade.tiff":
            cmap = "gray"
        elif name == "brecon_slope.tiff":
            cmap = "terrain"
        elif name == "brecon_aspect.tiff":
            cmap = "hsv"
        elif name == "brecon_curvature.tiff":
            cmap = "RdBu"
            vmin = np.nanpercentile(data, 5)
            vmax = np.nanpercentile(data, 95)

        plt.figure(figsize=(6, 6))
        im = plt.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)
        plt.title(name.split("_")[1].split(".")[0].capitalize())
        plt.axis("off")
        plt.colorbar(im)

        output_dir = "./storage/maps"
        os.makedirs(output_dir, exist_ok=True)
        output_img_path = os.path.join(output_dir, f"{name.split('.')[0]}.png")
        plt.savefig(output_img_path)
        plt.close()
        print(f"Saved {name} map to {output_img_path}")
