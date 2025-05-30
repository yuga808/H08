import numpy as np
import pandas as pd
import os

# === Settings ===
file_path = "../../map/out/riv_nxl_/rivnxl.CAMA.g5o"
output_dir = "../../lnd/csv"
os.makedirs(output_dir, exist_ok=True)
base_name = os.path.splitext(os.path.basename(file_path))[0]
csv_output = os.path.join(output_dir, base_name + ".csv")

# === Grid shape (for 2D files)
GRID_SHAPE = (2160, 4320)  # (rows, cols) for global 5-min grid

# === Read binary file
data = np.fromfile(file_path, dtype=np.float32)
L = data.size

# === Auto detect and reshape if needed
if L == GRID_SHAPE[0] * GRID_SHAPE[1]:
    # 2D case
    data_2d = data.reshape(GRID_SHAPE)
    df = pd.DataFrame(data_2d)
    df.to_csv(csv_output, index=False, header=False)
    print(f"[DONE] Saved 2D CSV: {csv_output} ({GRID_SHAPE[0]} x {GRID_SHAPE[1]})")
else:
    # 1D case
    df = pd.DataFrame({
        "L_index": np.arange(1, L + 1),
        "value": data
    })
    df.to_csv(csv_output, index=False)
    print(f"[DONE] Saved 1D CSV: {csv_output} ({L} values)")