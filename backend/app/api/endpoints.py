import os
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile
from backend.app.services.process_raster import process_terrain
from app.services.create_maps import create_maps

router = APIRouter()

UPLOAD_DIR = "./storage/raw"


def get_image_urls():
    base_url = "http://127.0.0.1:8000/images"
    pngs = os.listdir("./storage/maps")
    url = {name.split(".")[0]: f"{base_url}/{name}" for name in pngs}
    return url


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
def process_terrain_endpoint():
    try:
        example_file = "brecon_dem_27700.tif"
        process_terrain(example_file)
        create_maps()
        url = get_image_urls()
        print("Generated image URLs:", url)
        return {"images": url}
    except Exception as e:
        print(f"Error processing example terrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-terrain-from-file")
def process_terrain_from_file_endpoint(tif_file: UploadFile = File(...)):
    try:
        upload_file(tif_file)
        process_terrain(tif_file.filename)
        create_maps()
        url = get_image_urls()
        return {"images": url}
    except Exception as e:
        print(f"Error processing terrain from file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
