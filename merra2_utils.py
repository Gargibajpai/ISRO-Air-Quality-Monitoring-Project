import xarray as xr
import numpy as np
from datetime import datetime, timedelta

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def get_met_data(lat, lon, date, nc4_path):
    """
    Extract meteorological data from a MERRA-2 .nc4 file for a given lat/lon and date.
    Args:
        lat (float): Latitude
        lon (float): Longitude
        date (datetime.date): Date
        nc4_path (str): Path to the .nc4 file
    Returns:
        dict: {'temperature': float (deg C), 'humidity': float (%), 'wind_speed': float (km/h)}
    """
    ds = xr.open_dataset(nc4_path)
    # Find nearest lat/lon indices
    lat_idx = find_nearest(ds['lat'].values, lat)
    lon_idx = find_nearest(ds['lon'].values, lon)
    # Find nearest time index (assume time is in hours since a ref date)
    # Convert date to numpy datetime64 for comparison
    times = ds['time'].values
    # If time is in hours since ref, convert to datetime64
    if np.issubdtype(times.dtype, np.datetime64):
        date64 = np.datetime64(datetime(date.year, date.month, date.day))
        time_idx = find_nearest(times, date64)
    else:
        # fallback: just use first time index
        time_idx = 0
    # Extract variables
    t2m = float(ds['T2M'][time_idx, lat_idx, lon_idx]) - 273.15  # Kelvin to Celsius
    rh2m = float(ds['RH2M'][time_idx, lat_idx, lon_idx])         # %
    u2m = float(ds['U2M'][time_idx, lat_idx, lon_idx])           # m/s
    v2m = float(ds['V2M'][time_idx, lat_idx, lon_idx])           # m/s
    wind_speed = np.sqrt(u2m**2 + v2m**2) * 3.6                 # m/s to km/h
    ds.close()
    return {
        'temperature': round(t2m, 1),
        'humidity': round(rh2m, 1),
        'wind_speed': round(wind_speed, 1)
    } 