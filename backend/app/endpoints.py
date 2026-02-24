from fastapi import APIRouter, HTTPException
from app.services.process_dem import calculate_terrain
from app.services.create_maps import create_maps

router = APIRouter()


@router.get("/process-example")
def calculate_terrain_example_endpoint():
    try:
        calculate_terrain()
        create_maps()
        base_url = "http://127.0.0.1:8000/images"
        pngs = [
            "brecon_slope.png",
            "brecon_aspect.png",
            "brecon_hillshade.png",
            "brecon_curvature.png",
        ]
        url = {name.split(".")[0].split("_")[1]: f"{base_url}/{name}" for name in pngs}
        print("Generated image URLs:", url)
        return {"message": "Terrain processed and maps created", "images": url}
    except Exception as e:
        print(f"Error processing terrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/process-terrain")
# def calculate_terrain_endpoint():
#     try:
#         calculate_terrain()
#     except Exception as e:
#         print(f"Error processing terrain: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/process-maps")
# def create_maps_endpoint():
#     try:
#         create_maps()

#     except Exception as e:
#         print(f"Error processing maps: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
