import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import os

# === USER SETTINGS ===
GRID = "5min"            # Options: "30min", "5min", etc.
APPLY_FLIP = False       # True to flip vertically (upsidedown)
SAVE_PNG = False          # Save to ../png/

file_paths = [
#    "../../map/dat/lnd_msk_/lndmsk.CAMA.g5o",
#    "../../map/dat/lnd_ara_/lndara.CAMA.g5o",
#    "../../lnd/dat/uniform.1.00.g5o",
#    "../../lnd/dat/uniform.0.30.g5o",
#    "../../lnd/dat/uniform.0.15.g5o",
#    "../../lnd/dat/uniform.13000.00.g5o",
#    "../../lnd/dat/uniform.0.003.g5o",
#    "../../lnd/dat/gamma___/isim____00000000.g5o",
#    "../../lnd/dat/tau_____/isim____00000000.g5o",
#    "../../map/dat/Albedo__/GSW2____00000100.g5o",
#    "../../lnd/dat/uniform.2.00.g5o",
#    "../../lnd/dat/uniform.100.00.g5o",
#    "../../lnd/dat/gwr_____/fg.g5o",
#    "../../lnd/dat/gwr_____/rgmax.g5o",
#    "../../met/dat/Wind____/isim____20410100.g5o",
#    "../../met/dat/Rainf___/isim____20410000.g5o",
#    "../../met/dat/Snowf___/isim____20410100.g5o",
#    "../../met/dat/PSurf___/isim____20410100.g5o",
#    "../../met/dat/Tair____/isim____20410100.g5o",
#    "../../met/dat/Qair____/isim____20410100.g5o",
#    "../../met/dat/LWdown__/isim____20410100.g5o",
#    "../../met/dat/SWdown__/isim____20410100.g5o",
#    "../../lnd/ini/uniform.150.0.g5o",
#    "../../lnd/ini/uniform.283.15.g5o",
#    "../../lnd/ini/uniform.0.0.g5o",
#    "../../lnd/out/SoilMois/ISIMLR__20401200.g5o",
#    "../../lnd/out/SoilMois/ISIMLR__20501200.g5o",
#    "../../cpl/pst/evap_cleaned.g5o",
#    "../../lnd/out/SoilTemp/ISIMLR__20410100.g5o",
#    "../../lnd/out/AvgSurfT/ISIMLR__20410100.g5o",
#    "../../lnd/out/SWE_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/GW______/ISIMLR__20410100.g5o",
#    "../../lnd/out/SWnet___/ISIMLR__20410100.g5o",
#    "../../lnd/out/LWnet___/ISIMLR__20410101.g5o",
#    "../../lnd/out/Qle_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qh______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qg______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qf______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qv______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Evap____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qs______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qsb_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qtot____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qtot____/ISIMN_C_20410100.g5o",
#    "../../lnd/out/PotEvap_/ISIMLR__20410100.g5o",
#    "../../lnd/out/SubSnow_/ISIMLR__20410100.g5o",
#    "../../lnd/out/SAlbedo_/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qrc_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qbf_____/ISIMLR__20410100.g5o",
#    "../../riv/dat/uniform.0.5.g5o",
#    "../../riv/dat/uniform.1.4.g5o",
#    "../../map/out/riv_nxl_/rivnxl.CAMA.g5o",
#    "../../map/out/riv_mou_/rivmou.CAMA.g5o",
#    "../../map/out/riv_seq_/rivseq.CAMA.g5o",
#    "../../map/out/des_pot_/Hist____20050000.CAMA.14000.0.08.g5o",
#    "../../riv/out/riv_out_/ISIMLR__20410100.g5o",
#    "../../riv/out/riv_sto_/ISIMLR__20410100.g5o",
#    "../../cpl/pst/temp.g5o",
#    "../../cpl/pst/temp.g5o.nan0",
#    "../../cpl/pst/temp.gwbal.g5o",
#    "../../cpl/pst/temp.lndara.g5o",
#    "../../cpl/pst/temp.lndbal.g5o",
#    "../../cpl/pst/temp.mask.g5o",
#    "../../cpl/pst/temp.swbal.g5o",
#    "../../map/dat/flw_dir_/flwdir.CAMA.g5o",
#    "/home/kajiyama/H08/H08_20230612/map/dat/lnd_msk_/lndmsk.CAMA.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/uniform.1.00.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/gamma___/W5E5____00000000.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/tau_____/W5E5____00000000.g5o",
#    "/home/kajiyama/H08/H08_20230612/map/dat/Albedo__/GSW2____00000100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/uniform.2.00.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/gwr_____/fg.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/dat/gwr_____/rgmax.g5o",
#    "/home/kajiyama/H08/H08_20230612/met/dat/Wind____/W5E5____20010101.g5o",
#    "/home/kajiyama/H08/H08_20230612/met/dat/SWdown__/W5E5____20010101.g5o",
#    "/home/kajiyama/H08/H08_20230612/met/dat/Tair____/W5E5____20010101.g5o",
#    "/home/kajiyama/H08/H08_20230612/met/dat/Qair____/W5E5____20010101.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/ini/uniform.150.0.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/ini/uniform.283.15.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/ini/uniform.0.0.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/SAlbedo_/W5E5LR__20010000.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/SoilMois/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/SoilTemp/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/AvgSurfT/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/SWE_____/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/GW______/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/SWnet___/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/LWnet___/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qle_____/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qh______/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qg______/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qf______/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qv______/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Evap____/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qs______/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qsb_____/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qtot____/W5E5LR__20010000.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/PotEvap_/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/SubSnow_/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/SAlbedo_/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qrc_____/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qbf_____/W5E5LR__20010100.g5o",
#    "/home/kajiyama/H08/H08_20230612/riv/out/riv_out_/W5E5LR__20140100.g5o",
#    "/home/kajiyama/H08/H08_20230612/riv/out/riv_sto_/W5E5LR__20140100.g5o",

#    "../../crp/out/crp_ric_/ISIM__C_00000000.g5o",
#    "../../crp/out/hvs_ric_/ISIM__C_00000000.g5o",
#    "../../crp/out/plt_ric_/ISIM__C_00000000.g5o",
#    "../../crp/out/yld_ric_/ISIM__C_00000000.g5o",

#    "../../riv/out/riv_out_/ISIMN_C_20410101.g5o",
#    "../../dam/out/dam_out_/ISIMN_C_20410100.g5o",
#    "../../lnd/out/AvgSurfT/ISIMN_C_20410100.g5o",
#    "../../lnd/out/SupAgr__/ISIMN_C_20410100.g5o",
#    "../../lnd/out/DemAgr__/ISIMN_C_20410100.g5o",
#    "../../lnd/out/Qtot____/ISIMN_C_20410100.g5o",

#    "../../map/out/crp_typ1/M08_____20000000.g5o",
#    "../../map/out/crp_typ2/M08_____20000000.g5o",
#    "../../map/out/can_org_/canorg.l.merged.1.CAMA.g5o",

    "../../lnd/out/Qtot____/ISIMN_C_20410100.g5o",
#    "../../lnd/out/Qtot____/ISIMLR__20410000.g5o",


]

# === Grid settings ===
if GRID == "30min":
    lat_res = 0.5
    lon_res = 0.5
    nx, ny = 720, 360
    l2x_path = "../../map/dat/l2x_l2y_/l2x.hlo.txt"
    l2y_path = "../../map/dat/l2x_l2y_/l2y.hlo.txt"
elif GRID == "5min":
    lat_res = 0.083333
    lon_res = 0.083333
    nx, ny = 4320, 2160
    l2x_path = "../../map/dat/l2x_l2y_/l2x.g5o.txt"
    l2y_path = "../../map/dat/l2x_l2y_/l2y.g5o.txt"
else:
    raise ValueError("Unsupported grid resolution")

#l2x = np.loadtxt(l2x_path, dtype=int) - 1
#l2y = np.loadtxt(l2y_path, dtype=int) - 1
l2x = np.loadtxt(l2x_path, dtype=float).astype(np.int64) - 1
l2y = np.loadtxt(l2y_path, dtype=float).astype(np.int64) - 1
nl = len(l2x)

# === Coordinate Grid ===
lats = np.linspace(90 - lat_res / 2, -90 + lat_res / 2, ny)
lons = np.linspace(-180 + lon_res / 2, 180 - lon_res / 2, nx)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# === Plot Setup ===
n = len(file_paths)
cols = 2 if n > 1 else 1
rows = (n + cols - 1) // cols
fig_size = (14, 7 * rows) if n > 1 else (10, 5)
fig, axes = plt.subplots(rows, cols, figsize=fig_size, subplot_kw={'projection': ccrs.PlateCarree()})
axes = np.atleast_1d(axes).flatten()

# === Draw each file ===
for i, path in enumerate(file_paths):
    ax = axes[i]
    dir_name = os.path.basename(os.path.dirname(path))
    file_name = os.path.basename(path)

    if not os.path.exists(path):
        ax.set_title(f"File not found\n{dir_name}/{file_name}")
        ax.axis("off")
        continue

    data = np.fromfile(path, dtype=np.float32, count=nl)
    r2dat = np.full((ny, nx), np.nan, dtype=np.float32)
    for j in range(nl):
        x = l2x[j]
        y = l2y[j]
        r2dat[y, x] = data[j]

    if APPLY_FLIP:
        r2dat = r2dat[::-1, :]
    r2dat[r2dat <= 0] = np.nan

    if np.all(np.isnan(r2dat)):
        ax.set_title(f"All data is NaN\n{dir_name}/{file_name}")
        ax.axis("off")
        continue

    try:
        vmin = np.nanpercentile(r2dat, 5)
        vmax = np.nanpercentile(r2dat, 95)
        pcm = ax.pcolormesh(
            lon_grid, lat_grid, r2dat,
            cmap="plasma",
            norm=LogNorm(vmin=vmin, vmax=vmax),
            shading="auto", transform=ccrs.PlateCarree()
        )
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.set_global()
        ax.set_title(f"{dir_name}/{file_name}")

        # === Individual colorbar ===
        cax = ax.inset_axes([1.02, 0.1, 0.02, 0.8])
        fig.colorbar(pcm, cax=cax, label="Log-scaled Value")
    except ValueError as e:
        ax.set_title(f"Invalid data range for LogNorm\n{dir_name}/{file_name}\n{e}")
        ax.axis("off")

# === Hide unused axes ===
for j in range(i + 1, len(axes)):
    axes[j].axis("off")

# === Layout adjustment ===
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
