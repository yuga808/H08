import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import os

# === Configuration ===
file_1d = "../../map/dat/flw_dir_/flwdir.CAMA.g5o"
#file_2d = "/home/kajiyama/H08/H08_20230612/map/dat/flw_dir_/flwdir.CAMA.gl5"
file_2d = "../../map/dat/flw_dir_/flwdir.CAMA.gl5"
file_l2x = '../../map/dat/l2x_l2y_/l2x.g5o.txt'
file_l2y = '../../map/dat/l2x_l2y_/l2y.g5o.txt'
resolution = '5min'
apply_flip = False
SAVE_PNG = False  # <- Change to False to disable saving

# === Resolution Mapping ===
res_config = {
    '5min':    {'nx': 4320, 'ny': 2160},
    '30min':   {'nx': 720,  'ny': 360},
    '0.25deg': {'nx': 1440, 'ny': 720},
}

nx = res_config[resolution]['nx']
ny = res_config[resolution]['ny']
nl = len(np.loadtxt(file_l2x, dtype=int))

# === Load Data ===
data_1d = np.fromfile(file_1d, dtype=np.float32, count=nl)
data_2d = np.fromfile(file_2d, dtype=np.float32).reshape((ny, nx))
if apply_flip:
    data_2d = data_2d[::-1, :]

l2x = np.loadtxt(file_l2x, dtype=int)
l2y = np.loadtxt(file_l2y, dtype=int)

# === Map 1D data to 2D and compute difference ===
diff_map = np.full((ny, nx), np.nan, dtype=np.float32)
for i in range(nl):
    x = l2x[i] - 1
    y = l2y[i] - 1
    diff_map[y, x] = data_2d[y, x] - data_1d[i]

# === Plotting ===
fig, ax = plt.subplots(figsize=(14, 7), subplot_kw={'projection': ccrs.PlateCarree()})
lon = np.linspace(-180, 180, nx)
lat = np.linspace(-90, 90, ny)
lon_grid, lat_grid = np.meshgrid(lon, lat)

pcm = ax.pcolormesh(
    lon_grid, lat_grid, diff_map,
    cmap='bwr',
    shading='auto',
    transform=ccrs.PlateCarree()
)

ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_global()

# === Title and Colorbar ===
rel_path_1 = os.path.join(os.path.basename(os.path.dirname(file_1d)), os.path.basename(file_1d))
rel_path_2 = os.path.join(os.path.basename(os.path.dirname(file_2d)), os.path.basename(file_2d))
title_str = f"Difference Map: {rel_path_2} - {rel_path_1}"
ax.set_title(title_str)

fig.colorbar(pcm, ax=ax, label="Value Difference (2D - 1D)")

plt.tight_layout()

# === Save if enabled ===
if SAVE_PNG:
    os.makedirs("../png", exist_ok=True)
    base_title = f"{rel_path_2}_minus_{rel_path_1}".replace("/", "_")
    output_filename = f"../png/{base_title}.png"
    fig.savefig(output_filename, dpi=300)
    print(f"Saved image as: {output_filename}")

plt.show()

a = np.loadtxt("../../map/dat/l2x_l2y_/l2y.g5o.txt")
b = np.loadtxt("/home/kajiyama/H08/H08_20230612/map/dat/l2x_l2y_/l2y.g5o.txt")

if np.array_equal(a, b):
    print("perfectly")
else:
    print("zannen")

matches = np.sum(a == b)
total = len(a)
ratio = matches / total * 100

print(f"match total: {matches}/{total}")
print(f"match ratio: {ratio:.2f}%")
