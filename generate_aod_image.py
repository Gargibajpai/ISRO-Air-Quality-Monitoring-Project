import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 🔁 Replace with your actual .nc file
file_path = "E06OCM_L3_LAC_AD_20250615.nc"

# Load the dataset
ds = xr.open_dataset(file_path)

# Print to inspect variable names (run once)
print(ds.data_vars)

# Update this to your AOD variable name
aod = ds['AOD']  # Change if it's something like 'AOD_550nm'

# Plot and save
plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
aod.plot(ax=ax, cmap='plasma', cbar_kwargs={'label': 'AOD'})
ax.coastlines()
ax.add_feature(cfeature.BORDERS)
ax.set_title("AOD from EOS-06 (15 June 2025)")

# Save image
plt.savefig("aod_20250615.png", dpi=300, bbox_inches='tight')
plt.show()
