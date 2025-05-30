# -*- coding: utf-8 -*-
import numpy as np

# === Input settings ===
file_path = "../../met/out/Koppen__/isim____00000000.gl5"         # Input binary file
output_path = "../../met/out/Koppen__/isim____00000000.gl5"  # Output file
grid_shape = (2160, 4320)           # 5-minute global grid (rows, cols)

# === Load binary data as 2D float32
data = np.fromfile(file_path, dtype=np.float32)
assert data.size == grid_shape[0] * grid_shape[1], "Grid size mismatch!"
data = data.reshape(grid_shape)

# === Updates: dictionary with (row, col): new_value
# Indexes are 0-based: row x [0, 2159], col x [0, 4319]
updates = {
    (340, 3056): 42,
    (1864, 785): 51
}

# === Apply updates
for (row, col), value in updates.items():
    if 0 <= row < grid_shape[0] and 0 <= col < grid_shape[1]:
        data[row, col] = value
        print(f"Updated (row={row}, col={col}) to {value}")
    else:
        print(f"[WARNING] Index (row={row}, col={col}) out of bounds")

# === Save modified data back to binary file
data.astype(np.float32).tofile(output_path)
print(f"[DONE] Modified .gl5 saved to: {output_path}")
