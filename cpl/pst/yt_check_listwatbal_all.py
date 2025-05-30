import numpy as np
import matplotlib.pyplot as plt
import os

# === Input files grouped by variable ===
categories = {
    "PRCP": [f"../../met/dat/Rainf___/isim____{y}0000.g5o" for y in range(2041, 2051)] +
            [f"../../met/dat/Snowf___/isim____{y}0000.g5o" for y in range(2041, 2051)],
    "EVAP": [f"../../lnd/out/Evap____/ISIMLR__{y}0000.g5o" for y in range(2041, 2051)],
    "QTOT": [f"../../lnd/out/Qtot____/ISIMLR__{y}0000.g5o" for y in range(2041, 2051)],
    "DELSM": ["../../lnd/out/SoilMois/ISIMLR__20401200.g5o", "../../lnd/out/SoilMois/ISIMLR__20501200.g5o"],
    "DELSWE": ["../../lnd/out/SWE_____/ISIMLR__20401200.g5o", "../../lnd/out/SWE_____/ISIMLR__20501200.g5o"],
    "DELGW": ["../../lnd/out/GW______/ISIMLR__20401200.g5o", "../../lnd/out/GW______/ISIMLR__20501200.g5o"],
}

# === Constants ===
lndara_file = "../../map/dat/lnd_ara_/lndara.CAMA.g5o"
SECONDS_PER_YEAR = 86400 * 365
TO_KM3 = 1e-12

# === Load land area ===
if not os.path.exists(lndara_file):
    raise FileNotFoundError(f"{lndara_file} not found")
lndara = np.fromfile(lndara_file, dtype=np.float32)

# === Main plotting loop ===
for label, filelist in categories.items():
    data_by_file = []
    min_values = []

    for fpath in filelist:
        if not os.path.exists(fpath):
            print(f"[Missing] {fpath}")
            continue

        data = np.fromfile(fpath, dtype=np.float32)
        if data.size == lndara.size:
            data = data.reshape(-1)
        elif data.shape != lndara.shape:
            print(f"[Shape mismatch] {fpath}")
            continue

        valid = (data < 1e19) & (lndara > 0)
        flux_kg_s = data[valid] * lndara[valid]
        flux_km3_y = flux_kg_s * SECONDS_PER_YEAR * TO_KM3
        data_by_file.append(flux_km3_y)
        min_values.append(np.min(flux_km3_y))

    if data_by_file:
        plt.figure(figsize=(10, 6))
        bplot = plt.boxplot(data_by_file, showfliers=False)
        plt.title(f"{label} per Grid Cell (km3/year)")
        plt.xlabel("File Index")
        plt.ylabel("km3/year")
        plt.grid(True)

        # Add min value annotations
        for i, (x, val) in enumerate(zip(range(1, len(min_values)+1), min_values)):
            plt.text(x, val, f"{val:.2e}", ha='center', va='top', fontsize=8, color='blue')

        plt.tight_layout()
        plt.savefig(f"{label}_boxplot.png")
        plt.show()
        plt.close()
        print(f"[Saved] {label}_boxplot.png")
    else:
        print(f"[Skipped] {label}: no valid files")
