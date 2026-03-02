import os
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.process_raster import process_terrain
from app.services.create_maps import create_maps

router = APIRouter()

UPLOAD_DIR = "./storage/raw"


def mount_image_urls(saved_maps):
    base_url = "http://127.0.0.1:8000/images"
    urls = {}
    for name, path in saved_maps.items():
        filename = os.path.basename(path)
        urls[name] = f"{base_url}/{filename}"
    return urls


def upload_file(file: UploadFile):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"Uploaded file saved to {file_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process-terrain-example")
def process_terrain_example_endpoint():
    try:
        example_file = "brecon_dem.gtiff"
        process_terrain(example_file)
        saved_maps = create_maps()
        urls = mount_image_urls(saved_maps)
        return {"images": urls}
    except Exception as e:
        print(f"Error processing example terrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-terrain-from-file")
def process_terrain_from_file_endpoint(tif_file: UploadFile = File(...)):
    try:
        upload_file(tif_file)
        process_terrain(tif_file.filename)
        saved_maps = create_maps()
        urls = mount_image_urls(saved_maps)
        return {"images": urls}
    except Exception as e:
        print(f"Error processing terrain from file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
