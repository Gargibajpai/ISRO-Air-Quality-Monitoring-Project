import rasterio
import numpy as np

def read_aod_geotiff(tif_path):
    with rasterio.open(tif_path) as src:
        aod = src.read(1)  # Read first band
        profile = src.profile
        transform = src.transform
    return aod, profile, transform

def get_aod_at_latlon(tif_path, lat, lon):
    with rasterio.open(tif_path) as src:
        row, col = src.index(lon, lat)
        aod_value = src.read(1)[row, col]
    return aod_value 