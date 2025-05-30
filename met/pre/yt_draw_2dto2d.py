import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import os

# === Settings ===
SAVE_PNG = False
APPLY_FLIP = False  # upsidedown (True:upsidedown)
# 30min
lat_res = 0.5
lon_res = 0.5

# 5min
lat_res = 0.083333
lon_res = 0.083333

nlat = int(180 / lat_res)
nlon = int(360 / lon_res)


# === Coordinate Grids ===
lats = np.linspace(90 - lat_res / 2, -90 + lat_res / 2, nlat)
lons = np.linspace(-180 + lon_res / 2, 180 - lon_res / 2, nlon)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# === File Paths ===
file_paths = [
#    "../../map/dat/lnd_msk_/lndmsk.CAMA.gl5",
#    "/home/kajiyama/H08/H08_20230612/map/dat/lnd_msk_/lndmsk.CAMA.gl5",
#    "../../map/dat/lnd_ara_/lndara.CAMA.gl5",
#    "../../met/dat/LWdown__/isim____20510101.hlf",
#    "../../met/dat/Rainf___/isim____20410100.gl5",
#    "../../met/dat/Rainf___/isim____20410000.hlf",
#    "../../met/dat/Prcp____/isim____20410100.gl5", 
#    "../../met/dat/Tair____/isim____20410100.gl5", 
#    "../../lnd/ini/uniform.150.0.gl5",
#    "../../lnd/ini/uniform.283.15.gl5",
#    "../../lnd/ini/uniform.0.0.gl5",
#    "../../lnd/dat/uniform.1.00.gl5",
#    "../../lnd/dat/uniform.0.30.gl5",
#    "../../lnd/dat/uniform.0.15.gl5",
#    "../../met/out/Koppen__/isim____00000000.gl5",
#    "../../met/out/Koppen__/W5E5____00000000.gl5",
#    "../../map/dat/soi_typ_/GSWP3___00000000.gl5",
#    "../../lnd/dat/gamma___/isim____00000000.gl5",
#    "../../lnd/dat/gwr_____/fg.gl5",
#    "../../map/out/riv_nxl_/rivnxl.CAMA.gl5",
#    "../../map/out/riv_mou_/rivmou.CAMA.gl5",
#    "../../lnd/out/SoilTemp/ISIMLR__20410100.gl5",
#    "../../lnd/out/Evap____/ISIMLR__20410000.gl5",
#    "../../lnd/out/Qtot____/ISIMLR__20410000.gl5",
#    "../../map/out/riv_mou_/rivmou.CAMA.gl5",
#    "../../riv/ini/uniform.0.0.gl5",
#    "../../map/dat/flw_dir_/flwdir.CAMA.gl5",
#    "../../map/out/riv_seq_/rivseq.WFDEI.hlf",
#    "../../map/out/riv_seq_/rivseq.CAMA.gl5",
#    "/home/kajiyama/H08/H08_20230612/lnd/ini/uniform.150.0.gl5",
#    "/home/kajiyama/H08/H08_20230612/lnd/ini/uniform.0.0.gl5",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/uniform.0.15.gl5",
#    "/home/kajiyama/H08/H08_20230612/met/out/Koppen__/W5E5____00000000.gl5",
#    "/home/kajiyama/H08/H08_20230612/map/dat/soi_typ_/GSWP3___00000000.gl5",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/gwr_____/fg.gl5",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/gamma___/W5E5____00000000.gl5",
#    "/home/kajiyama/H08/H08_20230612/riv/out/riv_sto_/W5E5LR__20000100.gl5",
#    "/home/kajiyama/H08/H08_20230612/map/out/riv_mou_/rivmou.CAMA.gl5",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/LWnet___/W5E5N_C_19840800.hlf",
#    "/home/kajiyama/H08/H08_20230612/riv/ini/uniform.0.0.gl5",
#    "/home/kajiyama/H08/H08_20230612/map/out/riv_seq_/rivseq.CAMA.gl5",
#    "/home/kajiyama/H08/H08_20230612/map/dat/flw_dir_/flwdir.CAMA.gl5",
#    "/home/kajiyama/H08/H08_20230612/riv/out/riv_out_/W5E5LR__20140100.gl5",
#    "/home/kajiyama/H08/H08_20230612/riv/out/riv_sto_/W5E5LR__20140100.gl5",
#    "../../met/dat/LWdown__/W5E5____20110100.hlf",
#    "../../map/out/can_org_/canorg.l.merged.ext.1.CAMA.gl5",
#    "../../map/out/can_org_/canorg.l.merged.6.CAMA.gl5",
    
]

# === Plot Setup ===
n = len(file_paths)
cols = 2 if n > 1 else 1
rows = (n + cols - 1) // cols
fig_size = (14, 7 * rows) if n > 1 else (10, 5)
fig, axes = plt.subplots(rows, cols, figsize=fig_size, subplot_kw={'projection': ccrs.PlateCarree()})
axes = np.atleast_1d(axes).flatten()

for i, path in enumerate(file_paths):
    ax = axes[i]
    if not os.path.exists(path):
        ax.set_title("File not found")
        ax.axis("off")
        continue

    data = np.fromfile(path, dtype=np.float32).reshape((nlat, nlon))
    if APPLY_FLIP:
        data = data[::-1, :]

    data[data <= 0] = np.nan

    pcm = ax.pcolormesh(
        lon_grid, lat_grid, data,
        cmap="plasma",
        norm=LogNorm(vmin=np.nanpercentile(data, 5), vmax=np.nanpercentile(data, 95)),
        shading="auto", transform=ccrs.PlateCarree()
    )

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_global()

    dir_name = os.path.basename(os.path.dirname(path))
    file_name = os.path.basename(path)
    ax.set_title(f"{dir_name}/{file_name}")

    # === Individual colorbar for each plot ===
    cax = ax.inset_axes([1.02, 0.1, 0.02, 0.8])  # [left, bottom, width, height]
    fig.colorbar(pcm, cax=cax, label="Log-scaled Value")

# Hide unused axes
for j in range(i + 1, len(axes)):
    axes[j].axis("off")

# Layout adjustment
if len(file_paths) == 1:
    fig.subplots_adjust(left=0.05, right=0.88, top=0.95, bottom=0.1)
else:
    plt.tight_layout()

# === Save if enabled ===
if SAVE_PNG:
    os.makedirs("../../met/png", exist_ok=True)
    if len(file_paths) == 1:
        base_title = f"{dir_name}_{file_name}".replace("/", "_")
        output_filename = f"../../met/png/{base_title}.png"
    else:
        base_titles = [
            f"{os.path.basename(os.path.dirname(p))}_{os.path.basename(p)}".replace("/", "_")
            for p in file_paths
        ]
        combined_name = "_and_".join(base_titles)
        output_filename = f"../../met/png/{combined_name}.png"

    fig.savefig(output_filename, dpi=300)
    print(f"Saved image as: {output_filename}")

plt.show()