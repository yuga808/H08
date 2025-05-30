import numpy as np
import rasterio
from rasterio.transform import Affine
import os

# === USER SETTINGS ===
GRID = "5min"            # Options: "30min" or "5min"
APPLY_FLIP = False       # True to flip vertically if needed
file_paths = [
#    "../../met/dat/Wind____/isim____20410101.g5o",
#    "../../met/dat/Rainf___/isim____20410101.g5o",
#    "../../met/dat/Snowf___/isim____20410101.g5o",
#    "../../met/dat/Tair____/isim____20410101.g5o",
#    "../../met/dat/Qair____/isim____20410101.g5o",
#    "../../met/dat/PSurf___/isim____20410101.g5o",
#    "../../met/dat/SWdown__/isim____20410101.g5o",
#    "../../met/dat/LWdown__/isim____20410101.g5o",
#    "../../map/dat/lnd_msk_/lndmsk.CAMA.g5o",
#    "../../map/dat/Albedo__/GSW2____00000100.g5o",
#    "../../lnd/dat/uniform.1.00.g5o",
#    "../../lnd/dat/uniform.0.30.g5o",
#    "../../lnd/dat/uniform.0.15.g5o",
#    "../../lnd/dat/uniform.13000.00.g5o",
#    "../../lnd/dat/uniform.0.003.g5o",
#    "../../lnd/dat/gamma___/isim____00000000.g5o",
#    "../../lnd/dat/tau_____/isim____00000000.g5o",
#    "../../lnd/dat/uniform.1.00.g5o",
#    "../../lnd/dat/uniform.0.30.g5o",
#    "../../lnd/dat/uniform.2.00.g5o",
#    "../../lnd/dat/uniform.100.00.g5o",
#    "../../lnd/dat/gwr_____/fg.g5o",
#    "../../lnd/dat/gwr_____/rgmax.g5o",
#    "../../lnd/ini/uniform.150.0.g5o",
#    "../../lnd/ini/uniform.283.15.g5o",
#    "../../lnd/ini/uniform.0.0.g5o",
#    "../../lnd/ini/uniform.283.15.g5o",
#    "../../lnd/ini/uniform.0.0.g5o"

#    "../../met/dat/Wind____/isim____20410100.g5o",
#    "../../met/dat/Rainf___/isim____20410100.g5o",
#    "../../met/dat/Snowf___/isim____20410100.g5o",
#    "../../met/dat/Tair____/isim____20410100.g5o",
#    "../../met/dat/Qair____/isim____20410100.g5o",
#    "../../met/dat/PSurf___/isim____20410100.g5o",
#    "../../met/dat/SWdown__/isim____20410100.g5o",
#    "../../met/dat/LWdown__/isim____20410100.g5o",
    
#    "../../lnd/out/SoilTemp/ISIMLR__20410100.g5o",
#    "../../lnd/out/AvgSurfT/ISIMLR__20410100.g5o",
#    "../../lnd/out/SWE_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/GW______/ISIMLR__20410100.g5o",
#    "../../lnd/out/SWnet___/ISIMLR__20410100.g5o",
#    "../../lnd/out/LWnet___/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qle_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qh______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qg______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qf______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qv______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Evap____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qs______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qsb_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qtot____/ISIMLR__20410100.g5o",
#    "../../lnd/out/PotEvap_/ISIMLR__20410100.g5o",
#    "../../lnd/out/SubSnow_/ISIMLR__20410100.g5o",
#    "../../lnd/out/SAlbedo_/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qrc_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qbf_____/ISIMLR__20410100.g5o",

#   "../../map/dat/flw_dir_/flwdir.CAMA.gl5",
#   "../../map/dat/flw_dir_/flwdir.CAMA.g5o",
#   "../../map/dat/flw_dir_/flwdir.WFDEI.hlf",
#   "../../map/dat/flw_dir_/flwdir.WFDEI.hlo",
#    "../../lnd/out/Qtot____/ISIMLR__20410000.g5o",
#    "/home/kajiyama/H08/H08_20230612/lnd/out/Qtot____/W5E5LR__20010000.g5o",
#    "../../map/out/riv_ara_/rivara.CAMA.g5o",
#    "../../map/out/riv_mou_/rivmou.CAMA.gl5",
#    "../../map/out/riv_num_/rivnum.CAMA.g5o",
#    "../../map/out/riv_nxd_/rivnxd.CAMA.g5o",
#    "../../map/out/riv_nxl_/rivnxl.CAMA.g5o",
#    "../../map/out/riv_seq_/rivseq.CAMA.g5o",
#    "../../map/out/riv_nxd_/rivnxd.WFDEI.hlf",
#    "/home/kajiyama/H08/H08_20230612/map/out/riv_nxd_/rivnxd.CAMA.gl5",
    "/home/kajiyama/H08/H08_20230612/map/out/riv_seq_/rivseq.CAMA.gl5",
#    "../../map/dat/lnd_ara_/lndara.CAMA.g5o",
#    "/home/kajiyama/H08/H08_20230612/map/dat/lnd_ara_/lndara.CAMA.gl5",
#    "../../riv/out/riv_out_/ISIMLR__20410100.g5o",
#    "../../riv/out/riv_sto_/ISIMLR__20410100.g5o",
#    "/home/kajiyama/H08/H08_20230612/riv/out/riv_out_/W5E5LR__20140100.gl5",
#    "/home/kajiyama/H08/H08_20230612/riv/out/riv_sto_/W5E5LR__20140100.gl5",



#    "../../cpl/pst/temp.lndbal.g5o",
#    "../../map/out/riv_ara_/rivara.CAMA.gl5.sanitized",
#    "../../map/out/riv_ara_/rivara.CAMA.g5o",
#    "../../map/out/crp_typ1/M08_____20000000.g5o",
#    "../../map/out/crp_typ2/M08_____20000000.g5o",

#    
]
output_dir = "../../../tiff"

# === GRID CONFIGURATION ===
if GRID == "30min":
    lat_res, lon_res = 0.5, 0.5
    nx, ny = 720, 360
    l2x_path = "../../map/dat/l2x_l2y_/l2x.hlo.txt"
    l2y_path = "../../map/dat/l2x_l2y_/l2y.hlo.txt"
elif GRID == "5min":
    lat_res, lon_res = 0.083333, 0.083333
    nx, ny = 4320, 2160
    l2x_path = "../../map/dat/l2x_l2y_/l2x.g5o.txt"
    l2y_path = "../../map/dat/l2x_l2y_/l2y.g5o.txt"
else:
    raise ValueError("Unsupported GRID resolution")

# Load 1D→2D index maps
l2x = np.loadtxt(l2x_path).astype(int) - 1
l2y = np.loadtxt(l2y_path).astype(int) - 1
nl = len(l2x)

# Prepare output directory
os.makedirs(output_dir, exist_ok=True)

# Define affine transform (upper-left corner at (-180, 90))
transform = Affine.translation(-180, 90) * Affine.scale(lon_res, -lat_res)

# Process each binary file
for path in file_paths:
    data = np.fromfile(path, dtype=np.float32)
    # Map to 2D grid if needed
    if data.size == nl:
        arr = np.full((ny, nx), np.nan, dtype=np.float32)
        for i in range(nl):
            arr[l2y[i], l2x[i]] = data[i]
    elif data.size == nx * ny:
        arr = data.reshape((ny, nx))
    else:
        raise ValueError(f"File size mismatch for {path}")

    if APPLY_FLIP:
        arr = np.flipud(arr)

    # Build output GeoTIFF path with full relative path in name
    rel_path = os.path.relpath(path, start="../../")  # Trim leading ../../
    name_flat = rel_path.replace("/", "_")  # Convert path to flat name
    root, ext = os.path.splitext(name_flat)
    ext_clean = ext[1:]  # remove leading dot
    out_file = os.path.join(output_dir, f"{root}_{ext_clean}.tif")
    
    # Write GeoTIFF
    with rasterio.open(
        out_file, 'w',
        driver='GTiff',
        height=ny, width=nx,
        count=1,
        dtype=arr.dtype,
        crs="EPSG:4326",
        transform=transform,
        nodata=np.nan
    ) as dst:
        dst.write(arr, 1)

        # === Add pyramids (overviews) ===
        overview_levels = [2, 4, 8, 16, 32]
        dst.build_overviews(overview_levels, resampling=rasterio.enums.Resampling.nearest)
        dst.update_tags(ns='rio_overview', resampling='nearest')

    print(f"Generated: {out_file}")


