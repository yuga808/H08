import xarray as xr
import rasterio
from rasterio.transform import from_origin
import numpy as np
import os
from datetime import datetime, timedelta

# Path to NetCDF file
nc_path = "../org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_rsds_global_daily_2041_2050.nc"

# Output directory
output_dir = "rsds_2041"
os.makedirs(output_dir, exist_ok=True)

# Open NetCDF file
ds = xr.open_dataset(nc_path)

# Time dimension
dates_str = ds['time'].dt.strftime('%Y-%m-%d').values

indices_2041 = [i for i, d in enumerate(dates_str) if d.startswith("2041-")]

from datetime import datetime
dates_2041 = [datetime.strptime(dates_str[i], '%Y-%m-%d') for i in indices_2041]

# Spatial information
lat = ds['lat'].values
lon = ds['lon'].values
res_lat = abs(lat[1] - lat[0])
res_lon = abs(lon[1] - lon[0])
transform = from_origin(lon.min(), lat.max(), res_lon, res_lat)

# Export each day as GeoTIFF
for i, idx in enumerate(indices_2041):
    rsds = ds['rsds'][idx, :, :]
    date = dates_2041[i]
    output_filename = f"rsds_{date.strftime('%Y-%m-%d')}.tif"
    output_path = os.path.join(output_dir, output_filename)

    with rasterio.open(
        output_path,
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

    print(f"Saved: {output_filename}")

