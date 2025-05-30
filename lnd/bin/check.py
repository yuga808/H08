import numpy as np

# === FILE PATHS ===
#file_fieldcap = "/home/kajiyama/H08/H08_20230612/lnd/dat/uniform.0.30.gl5"
#file_wilt     = "/home/kajiyama/H08/H08_20230612/lnd/dat/uniform.0.15.gl5"
#file_soildepth = "/home/kajiyama/H08/H08_20230612/lnd/dat/uniform.1.00.gl5"

file_fieldcap = "../../lnd/dat/uniform.0.30.gl5"
file_wilt     = "../../lnd/dat/uniform.0.15.gl5"
file_soildepth = "../../lnd/dat/uniform.1.00.gl5"

# === Read binary ===
def read_data(path, expected_length=None):
    data = np.fromfile(path, dtype=np.float32)
    if expected_length and len(data) != expected_length:
        print(f"Warning: Unexpected length in {path} -> {len(data)}")
    return data

# === Load data ===
fieldcap = read_data(file_fieldcap)
wilt = read_data(file_wilt)
soildepth = read_data(file_soildepth)

# === Check for invalid values ===
print("Field Capacity:")
print(" min:", np.min(fieldcap), " max:", np.max(fieldcap), " unique:", np.unique(fieldcap))

print("\nWilting Point:")
print(" min:", np.min(wilt), " max:", np.max(wilt), " unique:", np.unique(wilt))

print("\nSoil Depth:")
print(" min:", np.min(soildepth), " max:", np.max(soildepth), " unique:", np.unique(soildepth))

epsilon = 1e-10
denominator = soildepth * 1000 * (fieldcap - wilt)

print("\nDenominator stats:")
print(" min:", np.min(denominator), " max:", np.max(denominator))
print(" zero or near-zero count:", np.sum(np.abs(denominator) < epsilon))
print(" negative count:", np.sum(denominator < 0))
print(" NaN count:", np.sum(np.isnan(denominator)))
print(" Inf count:", np.sum(np.isinf(denominator)))

# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

# === SETTINGS ===
GRID = "5min"  # Options: "5min", "30min"
lat_res = 0.083333 if GRID == "5min" else 0.5
lon_res = 0.083333 if GRID == "5min" else 0.5
nx = 4320 if GRID == "5min" else 720
ny = 2160 if GRID == "5min" else 360
l2x_file = "../../map/dat/l2x_l2y_/l2x.g5o.txt" if GRID == "5min" else "../../map/dat/l2x_l2y_/l2x.hlo.txt"
l2y_file = "../../map/dat/l2x_l2y_/l2y.g5o.txt" if GRID == "5min" else "../../map/dat/l2x_l2y_/l2y.hlo.txt"

# === Load mapping files ===
l2x = np.loadtxt(l2x_file, dtype=int) - 1
l2y = np.loadtxt(l2y_file, dtype=int) - 1
nl = len(l2x)

# === Load 1D input data ===
def load_data(path):
    return np.fromfile(path, dtype=np.float32, count=nl)

depth = load_data("../../lnd/dat/uniform.1.00.g5o")
fieldcap = load_data("../../lnd/dat/uniform.0.30.g5o")
wilt = load_data("../../lnd/dat/uniform.0.15.g5o")
p0mis = 1.0e20

# === Compute denominator ===
denominator = depth * 1000 * (fieldcap - wilt)
bad_mask = (np.abs(denominator) < 1e-10) | np.isnan(denominator) | (denominator == p0mis)

# === Map to 2D grid ===
r2bad = np.full((ny, nx), np.nan, dtype=np.float32)
for i in range(nl):
    x = l2x[i]
    y = l2y[i]
    if bad_mask[i]:
        r2bad[y, x] = 1

# === Coordinate Grid ===
lon = np.linspace(-180 + lon_res / 2, 180 - lon_res / 2, nx)
lat = np.linspace(90 - lat_res / 2, -90 + lat_res / 2, ny)
lon_grid, lat_grid = np.meshgrid(lon, lat)

# === Plot ===
plt.figure(figsize=(13, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
pcm = ax.pcolormesh(lon_grid, lat_grid, r2bad, cmap="Reds", shading="auto", transform=ccrs.PlateCarree())
plt.colorbar(pcm, label="Invalid denominator (1 = error)")
plt.title("Grid cells where denominator ≈ 0 or invalid")
plt.tight_layout()
plt.show()

