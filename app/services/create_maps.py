import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os

processed_dir = "./storage/processed"
tiffs = ["brecon_aspect.tiff", "brecon_slope.tiff", "brecon_hillshade.tiff", "brecon_curvature.tiff"]

plt.figure(figsize=(12, 10))

for i, name in enumerate(tiffs, 1):
    path = os.path.join(processed_dir, name)
    with rasterio.open(path) as src:
        data = src.read(1)
        nodata = src.nodata
        data = np.where(data == nodata, np.nan, data)
    
    plt.subplot(2, 2, i)
    
    if name == "brecon_hillshade.tiff":
        cmap = "gray"
    elif name == "brecon_slope.tiff":
        cmap = "terrain"
    elif name == "brecon_aspect.tiff":
        cmap = "hsv"
    else: 
        cmap = "RdBu"
    
    im = plt.imshow(data, cmap=cmap)
    plt.title(name.split("_")[1].split(".")[0].capitalize())
    plt.axis("off")
    plt.colorbar(im, fraction=0.046, pad=0.04)

plt.tight_layout()
plt.show()