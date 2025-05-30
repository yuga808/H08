import numpy as np

# === FILE PATHS ===
input_file = "../../map/out/riv_nxl_/rivnxl.CAMA.gl5"       # Original .gl5 with 2D indices (values)
mask_file  = "../../map/dat/lnd_msk_/lndmsk.CAMA.gl5"       # Land mask (float32, 9331200 values)
output_file = "../../map/out/riv_nxl_/rivnxl.CAMA.g5o"      # Output .g5o with 1D indices (values)

# === GRID INFO ===
NX, NY = 4320, 2160
N2D = NX * NY

# === LOAD FILES ===
print("[INFO] Loading data and land mask...")
data_2d = np.fromfile(input_file, dtype=np.float32).astype(np.int32)  # values are 2D indices
lndmsk = np.fromfile(mask_file, dtype=np.float32)

if data_2d.size != N2D or lndmsk.size != N2D:
    raise ValueError("Size mismatch in input or mask")

# === BUILD 2D→1D INDEX MAP ===
land_indices = np.where(lndmsk == 1.0)[0]
flat2id_map = np.zeros(N2D, dtype=np.int32)
flat2id_map[land_indices] = np.arange(1, len(land_indices) + 1)

# === EXTRACT ORIGINAL VALUES FOR LAND CELLS ===
data_1d_original = data_2d[lndmsk == 1.0].astype(np.int32) - 1  # e.g. [503320, 493939, 503320, ...]

# === MAP THE ORIGINAL 2D TARGET INDICES TO 1D INDICES ===
data_1d_converted = np.where(
    (data_1d_original >= 0) & (data_1d_original < N2D),
    flat2id_map[data_1d_original],
    -1
)


# === SAVE TO OUTPUT ===
data_1d_converted.astype(np.float32).tofile(output_file)
print(f"[OK] Saved remapped file to: {output_file}")
print(f"[INFO] Total valid cells: {data_1d_converted.size}, missing: {(data_1d_converted < 0).sum()}")
