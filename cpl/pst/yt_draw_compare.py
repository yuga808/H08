# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import Normalize
import os

# === USER SETTINGS ===
MODE = "ratio"  # ← "diff" または "ratio" を選択
GRID = "5min"
VAR = "Prcp____"
PAST_DIR = "../../met/dat"
FUTURE_DIR = "../../met/dat"
SUF_PAST = "g5o"
SUF_FUTURE = "g5o"
PREFIX_PAST = "W5E5____"
PREFIX_FUTURE = "isim____"
YEARS_PAST = range(2011, 2019)
YEARS_FUTURE = range(2051, 2060)
MASK_PATH = "../../map/dat/lnd_msk_/lndmsk.CAMA.gl5"
APPLY_FLIP = False
SAVE_PNG = False

# === GRID設定 ===
if GRID == "5min":
    lat_res = 0.083333
    lon_res = 0.083333
    nx, ny = 4320, 2160
    l2x_path = "../../map/dat/l2x_l2y_/l2x.g5o.txt"
    l2y_path = "../../map/dat/l2x_l2y_/l2y.g5o.txt"
else:
    raise ValueError("Unsupported grid setting")

l2x = np.loadtxt(l2x_path, dtype=float).astype(np.int64) - 1
l2y = np.loadtxt(l2y_path, dtype=float).astype(np.int64) - 1
nl = len(l2x)
land_mask = np.fromfile(MASK_PATH, dtype=np.float32).reshape((ny, nx))

def load_and_expand(path, format, l2x, l2y, nx, ny):
    if not os.path.exists(path): return None
    data = np.fromfile(path, dtype=np.float32)
    if format == "1d":
        r2 = np.full((ny, nx), np.nan, dtype=np.float32)
        for j in range(len(l2x)):
            x, y = l2x[j], l2y[j]
            if 0 <= x < nx and 0 <= y < ny:
                r2[y, x] = data[j]
        return r2
    elif format == "2d":
        return data.reshape((ny, nx))
    else:
        raise ValueError("Unknown format")

def load_decade_avg(years, basedir, varname, suf, format, l2x, l2y, nx, ny, prefix):
    acc = np.zeros((ny, nx), dtype=np.float64)
    count = 0
    for y in years:
        for m in range(1, 13):
            yyyymm = f"{y}{m:02d}00"
            path = f"{basedir}/{varname}/{prefix}{yyyymm}.{suf}"
            r2 = load_and_expand(path, format, l2x, l2y, nx, ny)
            if r2 is not None:
                acc += np.nan_to_num(r2)
                count += 1
    return acc / count if count > 0 else np.full((ny, nx), np.nan)
    
def load_yearly_avg_1d(years, basedir, varname, suf, l2x, l2y, nx, ny, prefix):
    acc = np.zeros((ny, nx), dtype=np.float64)
    count = 0
    for y in years:
        yyyymm = f"{y}0000"
        path = f"{basedir}/{varname}/{prefix}{yyyymm}.{suf}"
        if not os.path.exists(path): continue
        data = np.fromfile(path, dtype=np.float32)
        if data.size != len(l2x):
            print(f"Warning: {path} size mismatch: {data.size} != {len(l2x)}")
            continue
        r2 = np.full((ny, nx), np.nan, dtype=np.float32)
        for j in range(len(l2x)):
            x, y_ = l2x[j], l2y[j]
            if 0 <= x < nx and 0 <= y_ < ny:
                r2[y_, x] = data[j]
        acc += np.nan_to_num(r2)
        count += 1
    return acc / count if count > 0 else np.full((ny, nx), np.nan)

# === 平均読み込み ===
#past_avg = load_decade_avg(YEARS_PAST, PAST_DIR, VAR, SUF_PAST, "2d", l2x, l2y, nx, ny, prefix=PREFIX_PAST)
#past_avg = load_decade_avg(
#    YEARS_PAST, PAST_DIR, VAR, SUF_PAST, "1d", l2x, l2y, nx, ny, prefix=PREFIX_PAST
#)
#future_avg = load_decade_avg(YEARS_FUTURE, FUTURE_DIR, VAR, SUF_FUTURE, "1d", l2x, l2y, nx, ny, prefix=PREFIX_FUTURE)

past_avg = load_yearly_avg_1d(YEARS_PAST, PAST_DIR, VAR, SUF_PAST, l2x, l2y, nx, ny, prefix=PREFIX_PAST)
future_avg = load_yearly_avg_1d(YEARS_FUTURE, FUTURE_DIR, VAR, SUF_FUTURE, l2x, l2y, nx, ny, prefix=PREFIX_FUTURE)


# === 陸域マスク + 指定モードで比較 ===
if MODE == "diff":
    out_data = np.where((land_mask == 1) & np.isfinite(past_avg) & np.isfinite(future_avg),
                        future_avg - past_avg, np.nan)
    cmap = "RdBu"
    vmin, vmax = -5, 5
    label = f"{VAR} Difference"
    title = f"Absolute Difference in {VAR} (W5E5 2011_2019 vs ISIM 2041_2050)"
elif MODE == "ratio":
    with np.errstate(divide='ignore', invalid='ignore'):
        out_data = np.where((land_mask == 1) & (past_avg != 0) & np.isfinite(past_avg) & np.isfinite(future_avg),
                            (future_avg / past_avg - 1) * 100, np.nan)
    cmap = "coolwarm"
    vmin, vmax = -50, 50
    label = "Change (%)"
    title = f"Relative Change in {VAR} (W5E5 2011_2019 vs ISIM 2051_2060)"
else:
    raise ValueError("MODE must be 'diff' or 'ratio'")

if APPLY_FLIP:
    out_data = out_data[::-1, :]
    land_mask = land_mask[::-1, :]

# === 座標グリッド ===
lats = np.linspace(90 - lat_res / 2, -90 + lat_res / 2, ny)
lons = np.linspace(-180 + lon_res / 2, 180 - lon_res / 2, nx)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# === 描画 ===
fig, ax = plt.subplots(figsize=(14, 7), subplot_kw={'projection': ccrs.PlateCarree()})
pcm = ax.pcolormesh(lon_grid, lat_grid, out_data,
                    cmap=cmap, norm=Normalize(vmin=vmin, vmax=vmax),
                    shading="auto", transform=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_global()
ax.set_title(title)

cbar = fig.colorbar(pcm, ax=ax, orientation='vertical', shrink=0.6, pad=0.05)
cbar.set_label(label)
plt.tight_layout()

if SAVE_PNG:
    out_path = f"{VAR}_{MODE}_masked.png"
    plt.savefig(out_path, dpi=300)
    print(f"Saved image as: {out_path}")

plt.show()