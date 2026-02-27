import pytest
import numpy as np
from app.services.process_raster import (
    calculate_slope,
    calculate_aspect,
    calculate_hillshade,
    calculate_curvature,
)

gentle_slope_raster = np.array([[0, 1], [0, 1]])

dx = 1
dy = 1


def test_calculate_slope():
    slope, dz_dx, dz_dy = calculate_slope(gentle_slope_raster, dx, dy)
    print("Slope:", slope)
    print("dx:", dz_dx)
    print("dy:", dz_dy)
    assert np.all(
        slope > 0
    )  # np.all checks if all values in the array satisfy the condition
    assert np.all(dz_dx == 1)
    assert np.all(dz_dy == 0)
