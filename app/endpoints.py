from fastapi import APIRouter, HTTPException
from app.services.process_dem import calculate_terrain
from app.services.create_maps import create_maps

router = APIRouter()


@router.post("/process_terrain")
def calculate_terrain_endpoint():
    try:
        calculate_terrain()
    except Exception as e:
        print(f"Error processing terrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process_maps")
def create_maps_endpoint():
    try:
        create_maps()

    except Exception as e:
        print(f"Error processing maps: {e}")
        raise HTTPException(status_code=500, detail=str(e))
