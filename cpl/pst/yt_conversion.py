import numpy as np

# === Load all required files
lndmsk_2d = np.fromfile("../../map/dat/lnd_msk_/lndmsk.CAMA.gl5", dtype=np.float32)  # size = 2160*4320
lndmsk_1d = np.fromfile("../../map/dat/lnd_msk_/lndmsk.CAMA.g5o", dtype=np.float32)  # size = 2247551
lon_all = np.loadtxt("../../map/dat/l2x_l2y_/l2x.gl5.txt")
lat_all = np.loadtxt("../../map/dat/l2x_l2y_/l2y.gl5.txt")

# === Derive 2D→1D lookup
land_indices_2d = np.where(lndmsk_2d == 1.0)[0]  # 0-based

def from_L1d_to_coords(L1d):
    """Convert 1D land index (1-based) to lon, lat, and corresponding 2D index."""
    i = L1d - 1
    L2d = land_indices_2d[i]
    return {
        "L_1d": L1d,
        "L_2d": L2d + 1,
        "lon": lon_all[L2d],
        "lat": lat_all[L2d]
    }

def from_L2d_to_coords(L2d):
    """Convert 2D index (1-based) to lon, lat; and corresponding 1D index if land."""
    i = L2d - 1
    lon = lon_all[i]
    lat = lat_all[i]
    if lndmsk_2d[i] == 1.0:
        # It's a land cell — find 1D index
        L1d = np.where(land_indices_2d == i)[0][0] + 1
    else:
        L1d = None
    return {
        "L_2d": L2d,
        "lon": lon,
        "lat": lat,
        "L_1d": L1d
    }

def from_coords_to_L(lon_input, lat_input, tolerance=1e-4):
    """Find closest L_2d and L_1d for given lon/lat"""
    dists = np.sqrt((lon_all - lon_input)**2 + (lat_all - lat_input)**2)
    i = np.argmin(dists)
    L2d = i + 1
    if lndmsk_2d[i] == 1.0:
        L1d = np.where(land_indices_2d == i)[0][0] + 1
    else:
        L1d = None
    return {
        "input_lon": lon_input,
        "input_lat": lat_input,
        "closest_L2d": L2d,
        "closest_L1d": L1d,
        "actual_lon": lon_all[i],
        "actual_lat": lat_all[i]
    }

result = from_L1d_to_coords(503936)
print(result)