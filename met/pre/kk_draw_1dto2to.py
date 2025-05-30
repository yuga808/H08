import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import os

# === User Configuration ===
#input_file = '/home/kajiyama/H08/H08_20230612/met/dat/Rainf___/W5E5____00000000.g5o'
input_file = '../../met/dat/Prcp____/isim____20410100.g5o'
l2x_file   = '../../map/dat/l2x_l2y_/l2x.g5o.txt'
l2y_file   = '../../map/dat/l2x_l2y_/l2y.g5o.txt'
resolution = '5min'       # Options: '5min', '30min', '0.25deg', etc.
APPLY_FLIP = False         # Set True to vertically flip (upside-down)

# === Resolution Mapping ===
res_config = {
    '5min':    {'nx': 4320, 'ny': 2160},
    '30min':   {'nx': 720,  'ny': 360},
    '0.25deg': {'nx': 1440, 'ny': 720},
}

# === Get grid dimensions ===
nx = res_config[resolution]['nx']
ny = res_config[resolution]['ny']
nl = len(np.loadtxt(l2x_file, dtype=int))  # Auto-detect land points

# === Load 1D data and mask coordinates ===
data = np.fromfile(input_file, dtype=np.float32, count=nl)
l2x = np.loadtxt(l2x_file, dtype=int)
l2y = np.loadtxt(l2y_file, dtype=int)

# === Initialize 2D array and map 1D data ===
r2data = np.full((ny, nx), np.nan, dtype=np.float32)
for i in range(nl):
    x = l2x[i] - 1
    y = l2y[i] - 1
    r2data[y, x] = data[i]

# === Mask invalid or missing values ===
r2data[r2data <= 0] = np.nan
data_to_plot = r2data[::-1] if APPLY_FLIP else r2data

# === Plotting ===
plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Generate coordinate grids
lon = np.linspace(-180, 180, nx)
lat = np.linspace(-90, 90, ny)
lon_grid, lat_grid = np.meshgrid(lon, lat)

pcm = ax.pcolormesh(
    lon_grid, lat_grid, data_to_plot,
    cmap='plasma',
    norm=LogNorm(vmin=np.nanpercentile(data_to_plot, 5),
                 vmax=np.nanpercentile(data_to_plot, 95)),
    shading='auto',
    transform=ccrs.PlateCarree()
)

ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
plt.colorbar(pcm, label='Value (log scale)')
plt.title(os.path.basename(input_file))
plt.tight_layout()
plt.show()
