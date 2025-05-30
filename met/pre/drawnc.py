import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import os

# Define resolution and grid size
#lat_res = 0.5
#lon_res = 0.5
#nlat = int(180 / lat_res)
#nlon = int(360 / lon_res)


lat_res = 0.0833333  # 5 arcminutes
lon_res = 0.0833333
nlat = int(180 / lat_res)  # 2160
nlon = int(360 / lon_res)  # 4320


# Coordinate grids
lats = np.linspace(90 - lat_res / 2, -90 + lat_res / 2, nlat)
lons = np.linspace(-180 + lon_res / 2, 180 - lon_res / 2, nlon)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# === Manually specify multiple file paths ===
file_paths = [
    "../../met/dat/Rainf___/isim____20410100.gl5"
    # Add more paths as needed
]

for file_path in file_paths:
    # Read binary data
    data = np.fromfile(file_path, dtype=np.float32)
    data = data.reshape((nlat, nlon))
#   data = data[::-1, :]  # flip vertically if needed
    data[data <= 0] = np.nan

    # Plot
    plt.figure(figsize=(14, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())
    pcm = ax.pcolormesh(
        lon_grid, lat_grid, data,
        cmap="plasma",
        norm=LogNorm(vmin=np.nanpercentile(data, 5), vmax=np.nanpercentile(data, 95)),
        shading="auto",
        transform=ccrs.PlateCarree()
    )
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_global()

    # Extract directory name and filename for title
    dir_name = os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    ax.set_title(f"{dir_name}/{file_name}")

    plt.colorbar(pcm, ax=ax, label="Log-scaled Value")
    plt.tight_layout()
    plt.show()