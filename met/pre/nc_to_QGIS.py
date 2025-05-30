
import xarray as xr
import rasterio
from rasterio.transform import from_origin
import numpy as np

# Path to the NetCDF file in ../org/ISIMIP
nc_path = "../org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_rsds_global_daily_2041_2050.nc"

# Open the NetCDF file
ds = xr.open_dataset(nc_path)

# Select the rsds variable for the first day (time index 0)
rsds = ds['rsds'][0, :, :]

# Get latitude and longitude arrays
lat = ds['lat'].values
lon = ds['lon'].values

# Calculate resolution and geo-transform
res_lat = abs(lat[1] - lat[0])
res_lon = abs(lon[1] - lon[0])
transform = from_origin(lon.min(), lat.max(), res_lon, res_lat)

# Output file name
output_tif = "rsds_2041_2050.tif"

# Save as GeoTIFF
with rasterio.open(
    output_tif,
    "w",
    driver="GTiff",
    height=rsds.shape[0],
    width=rsds.shape[1],
    count=1,
    dtype=rsds.dtype,
    crs="EPSG:4326",
    transform=transform,
) as dst:
    dst.write(rsds.values, 1)

print(f"Saved: {output_tif}")

