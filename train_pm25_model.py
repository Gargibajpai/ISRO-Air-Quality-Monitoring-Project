import pandas as pd
import xarray as xr
import glob
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os
import requests

# List of MERRA-2 .nc4 file URLs to download if not present
MERRA2_URLS = [
    # Add your URLs here
    "https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4/2024/12/MERRA2_400.tavg1_2d_slv_Nx.20241226.nc4",
    "https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4/2024/12/MERRA2_400.tavg1_2d_slv_Nx.20241227.nc4",
    "https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4/2024/12/MERRA2_400.tavg1_2d_slv_Nx.20241228.nc4",
    "https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4/2024/12/MERRA2_400.tavg1_2d_slv_Nx.20241229.nc4",
    "https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4/2024/12/MERRA2_400.tavg1_2d_slv_Nx.20241230.nc4",
    "https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4/2024/12/MERRA2_400.tavg1_2d_slv_Nx.20241231.nc4",
    "https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/M2T1NXSLV.5.12.4/2025/01/MERRA2_400.tavg1_2d_slv_Nx.20250101.nc4",
    # ... add more URLs as needed ...
]

def download_merra2_files(urls):
    for url in urls:
        filename = url.split("/")[-1]
        if not os.path.exists(filename):
            print(f"Downloading {filename} ...")
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Downloaded {filename}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
        else:
            print(f"{filename} already exists, skipping download.")

# Download MERRA-2 files if not present
if __name__ == "__main__":
    download_merra2_files(MERRA2_URLS)

# Step 1: Load CPCB PM2.5 data
cpcb_df = pd.read_csv('cpcb_data.csv')
cpcb_df['Date'] = pd.to_datetime(cpcb_df['Date'])

# Step 2: Load and concatenate all MERRA-2 meteorological data files
nc_files = glob.glob('*.nc4')
if not nc_files:
    print("No MERRA-2 .nc4 files found in the directory. Please add them and rerun this script.")
    exit(1)

merra_dfs = []
for nc_file in nc_files:
    print(f"Loading {nc_file} ...")
    ds = xr.open_dataset(nc_file)
    # Example: extract temperature and humidity (update variable names as per your files)
    # Common MERRA-2 variable names: T2M (2-meter air temperature), RH2M (2-meter relative humidity)
    try:
        df = ds[['T2M', 'RH2M']].to_dataframe().reset_index()
        merra_dfs.append(df)
    except Exception as e:
        print(f"Error reading variables from {nc_file}: {e}")
        continue
merra_df = pd.concat(merra_dfs, ignore_index=True)

# Step 3: Preprocess
cpcb_df = cpcb_df.dropna().drop_duplicates()
merra_df = merra_df.dropna().drop_duplicates()

# Step 4: Merge on date (and location if possible)
# For now, merge on date only (update if you have lat/lon info in both)
merra_df['time'] = pd.to_datetime(merra_df['time'])
# If merra_df has 'lat' and 'lon', you could also merge on city coordinates

# We'll do a simple merge: for each city/date in CPCB, find the closest date in MERRA-2 (same day)
merged = pd.merge(
    cpcb_df,
    merra_df,
    left_on='Date',
    right_on='time',
    how='inner'
)

if merged.empty:
    print("No matching dates found between CPCB and MERRA-2 data. Check your files and date ranges.")
    exit(1)

# Step 5: Prepare features and label
# Use T2M (temperature) and RH2M (humidity) as features
X = merged[['T2M', 'RH2M']]
y = merged['PM2.5']

# Step 6: Train/test split and model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, predictions))

# Step 7: Save the model
joblib.dump(model, 'pm25_model.pkl')
print("Model saved as pm25_model.pkl") 