# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

# === File Settings ===
file_paths = [
    "../../met/dat/Rainf___/isim____20410100.hlf",   # Low-resolution binary file
    "../../met/dat/Rainf___/isim____20410100.gl5",  # High-resolution binary file
]
nx_list = [720, 4320]
ny_list = [360, 2160]
labels = ["30min", "5min"]  # Resolution labels for titles


# === Zoom Configuration ===
ZOOM_SCALE = 50  # Smaller = wider view

locations = {
    "Tokyo": {"lon": 139.6917, "lat": 35.6895},
    "London": {"lon": -0.1276, "lat": 51.5074},
    "Paris": {"lon": 2.3522, "lat": 48.8566},
    "Los Angeles": {"lon": -118.2437, "lat": 34.0522},
}
target_city = "Tokyo"  # Change to desired city

lon_center = locations[target_city]["lon"]
lat_center = locations[target_city]["lat"]

# === Manual color range ===
USE_MANUAL_COLOR_RANGE = True
VMIN = 0.0
VMAX = 0.0001

# === Plotting Zoomed-In Maps Only ===
fig, axes = plt.subplots(1, 2, figsize=(14, 7), subplot_kw={'projection': ccrs.PlateCarree()})

titles = []
for i, (path, nx, ny, label) in enumerate(zip(file_paths, nx_list, ny_list, labels)):
    ax = axes[i]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        ax.set_title("File not found")
        ax.axis("off")
        continue

    data = np.fromfile(path, dtype=np.float32).reshape((ny, nx))[::-1, :]
    data[data <= 0] = np.nan

    lon = np.linspace(-180, 180, nx)
    lat = np.linspace(-90, 90, ny)
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    pcm = ax.pcolormesh(
        lon_grid, lat_grid, data,
        cmap="plasma",
        shading="auto",
        transform=ccrs.PlateCarree(),
        vmin=VMIN if USE_MANUAL_COLOR_RANGE else None,
        vmax=VMAX if USE_MANUAL_COLOR_RANGE else None,
    )


    dlon = 360 / ZOOM_SCALE
    dlat = 180 / ZOOM_SCALE
    ax.set_extent(
    [lon_center - dlon, lon_center + dlon, lat_center - dlat, lat_center + dlat],
    crs=ccrs.PlateCarree()
    )


    dir_name = os.path.basename(os.path.dirname(path))
    file_name = os.path.basename(path)
    title_str = f"{label} - {target_city} ({dir_name}/{file_name})"
    ax.set_title(title_str, fontsize=10)
    titles.append(f"{dir_name}_{file_name}".replace("/", "_"))

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    cbar = fig.colorbar(pcm, ax=ax, orientation='horizontal', pad=0.07)
    cbar.set_label("Value")

plt.show()
plt.tight_layout()

# === Save figure ===
os.makedirs("../png", exist_ok=True)
filename = f"../png/{target_city}_{'_vs_'.join(titles)}.png"
fig.savefig(filename, dpi=300)
print(f"Saved image as: {filename}")