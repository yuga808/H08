import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# === SETTINGS ===
components = {
    "temp": "temp.g5o",      # Precipitation = Rainf + Snowf
    "gwbal": "temp.gwbal.g5o",      # Evapotranspiration
    "lndara": "temp.lndara.g5o",      # Total runoff
    "lndbal": "temp.lndbal.g5o",    # Change in Soil Moisture
    "mask": "temp.mask.g5o",  # Change in Snow Water Equivalent
    "swbal": "temp.swbal.g5o",    # Change in Groundwater
#    "BALLND": "temp.lndbal.g5o",  # Water balance error (should ≈ 0)
}

lndara_file = "../../map/dat/lnd_ara_/lndara.CAMA.g5o"  # Land area [m2]
SECONDS_PER_YEAR = 86400 * 365
TO_KM3 = 1e-12  # kg → km³

# === Load land area ===
if not os.path.exists(lndara_file):
    raise FileNotFoundError(f"{lndara_file} not found")
lndara = np.fromfile(lndara_file, dtype=np.float32)

# === Collect data per component ===
box_data = {}
for key, filepath in components.items():
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found")
        continue

    data = np.fromfile(filepath, dtype=np.float32)
    if data.shape != lndara.shape:
        print(f"Warning: Shape mismatch in {filepath}")
        continue

    valid = (data < 1e19) & (lndara > 0)
    flux_kg_s = data[valid] * lndara[valid]
    flux_km3_y = flux_kg_s * SECONDS_PER_YEAR * TO_KM3
    box_data[key] = flux_km3_y

# === Plot boxplot ===
plt.figure(figsize=(10, 6))
plt.boxplot([box_data[k] for k in box_data], labels=box_data.keys(), showfliers=False)
plt.ylabel("Flux per grid cell [km³/year]")
plt.title("Water Balance Components (Box Plot)")
plt.grid(True)
plt.tight_layout()
plt.show()


