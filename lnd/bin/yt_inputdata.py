# -*- coding: utf-8 -*-
import numpy as np
import os

# Fortran-style index (1-based)
target_index = 503936

# List of .g5o files with MO files set to 20410100
file_paths = [
#    # Static input
#    "../../map/dat/lnd_msk_/lndmsk.CAMA.g5o",
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
#    "../../met/out/Koppen__/isim____00000000.gl5",
#
#    # Initial condition input
#    "../../lnd/ini/uniform.150.0.g5o",
#    "../../lnd/ini/uniform.283.15.g5o",
#    "../../lnd/ini/uniform.0.0.g5o",
#
#    # Meteorological forcing (daily input)
#    "../../met/dat/Wind____/isim____20410101.g5o",
#    "../../met/dat/Rainf___/isim____20410101.g5o",
#    "../../met/dat/Snowf___/isim____20410101.g5o",
#    "../../met/dat/Tair____/isim____20410101.g5o",
#    "../../met/dat/Qair____/isim____20410101.g5o",
#    "../../met/dat/PSurf___/isim____20410101.g5o",
#    "../../met/dat/SWdown__/isim____20410101.g5o",
#    "../../met/dat/LWdown__/isim____20410101.g5o",
#
#    # Monthly output input (MO) corrected to 20410100
#    "../../lnd/out/SoilMois/ISIMLR__20410100.g5o",
#    "../../lnd/out/SoilTemp/ISIMLR__20410100.g5o",
#    "../../lnd/out/AvgSurfT/ISIMLR__20410100.g5o",
#    "../../lnd/out/SWE_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/SWnet___/ISIMLR__20410100.g5o",
#    "../../lnd/out/LWnet___/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qh______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qle_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qg______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qf______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qv______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qs______/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qsb_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/SubSnow_/ISIMLR__20410100.g5o",
#    "../../lnd/out/SAlbedo_/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qrc_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/Qbf_____/ISIMLR__20410100.g5o",
#    "../../lnd/out/GW______/ISIMLR__20410100.g5o",
#
#    # Daily output input (DY)
#    "../../lnd/out/Evap____/ISIMLR__20410101.g5o",
#    "../../lnd/out/Qtot____/ISIMLR__20410101.g5o",
#    "../../lnd/out/PotEvap_/ISIMLR__20410101.g5o",
#    
#    # River input
#    "../../riv/dat/uniform.0.5.g5o",
#    "../../riv/dat/uniform.1.4.g5o",
#    "../../riv/ini/uniform.0.0.g5o",
#    "../../map/out/riv_nxl_/rivnxl.CAMA.g5o",
#    "../../map/out/riv_mou_/rivmou.CAMA.g5o",
#    "../../map/out/des_pot_/Hist____20050000.CAMA.14000.0.08.g5o",
#    "../../riv/out/riv_out_/ISIMLR__20410100.g5o",
#    "../../riv/out/riv_sto_/ISIMLR__20410100.g5o",
    
#    "../../cpl/pst/temp.g5o",
#    "/home/kajiyama/H08/H08_20230612/cpl/pst/temp.g5o",
#    "../../cpl/pst/temp.gwbal.g5o",
#    "/home/kajiyama/H08/H08_20230612/cpl/pst/temp.gwbal.g5o",
#    "../../cpl/pst/temp.lndara.g5o",
#    "/home/kajiyama/H08/H08_20230612/cpl/pst/temp.lndara.g5o",
#    "../../cpl/pst/temp.lndbal.g5o",
#    "/home/kajiyama/H08/H08_20230612/cpl/pst/temp.lndbal.g5o",
#    "../../cpl/pst/temp.mask.g5o",
#    "/home/kajiyama/H08/H08_20230612/cpl/pst/temp.mask.g5o",
#    "../../cpl/pst/temp.swbal.g5o",
#    "/home/kajiyama/H08/H08_20230612/cpl/pst/temp.swbal.g5o",

    "/home/takahashi/H08/H08_20240718/crp/out/cwsb1st0/ISIMN_C_20410000.g5o", 
    
]

print(f"Checking index {target_index} in {len(file_paths)} files...\n")

for path in file_paths:
    try:
        data = np.fromfile(path, dtype=np.float32)
        if target_index <= len(data):
            value = data[target_index - 1]
            print(f"{path} -> {value:.6e}")
        else:
            print(f"{path} -> Index out of bounds (len = {len(data)})")
    except Exception as e:
        print(f"{path} -> Error: {e}")
        
import numpy as np
import matplotlib.pyplot as plt
import os  # os.path.basename用に必要

# ===== User Setting =====
file_path = "/home/takahashi/H08/H08_20240718/map/out/can_org_/canorg.l.merged.1.CAMA.g5o" # Path to the .g5o file
target_dtype = np.float32                    # Change to float64 if needed
missing_value = 1.0e20                       # 欠損値

# ===== Load Data =====
data = np.fromfile(file_path, dtype=target_dtype)
print(f"Loaded {len(data)} values from: {file_path}\n")

# ===== Extract Abnormal Indices =====
zero_indices = np.where(data == 0.0)[0]
missing_indices = np.where(data == missing_value)[0]

print(f"--- Abnormal Value Indices (1-based) ---")
print(f"Zero values      : {len(zero_indices)}")
for i in zero_indices[:10]:
    print(f"  Index: {i + 1}")
if len(zero_indices) > 10:
    print("  (Only first 10 shown)")

print(f"\nMissing values   : {len(missing_indices)}")
for i in missing_indices[:10]:
    print(f"  Index: {i + 1}")
if len(missing_indices) > 10:
    print("  (Only first 10 shown)")

# ===== Summary =====
total = len(data)
print("\n--- Summary ---")
print(f"Total cells      : {total}")
print(f"Zero-value cells : {len(zero_indices)} ({len(zero_indices)/total*100:.2f}%)")
print(f"Missing cells    : {len(missing_indices)} ({len(missing_indices)/total*100:.2f}%)")

# ===== Exclude Missing Values =====
data_valid = data[data < 1e10]

print(f"\nHistogram will be plotted using {len(data_valid)} non-missing values.")

# ===== Plot Histogram =====
plt.figure(figsize=(8, 5))
plt.hist(data_valid, bins=100, log=True, edgecolor='black')
plt.xlabel("Value")
plt.ylabel("Frequency (log scale)")
plt.title(f"Value Distribution (no missing): {os.path.basename(file_path)}")
plt.grid(True)
plt.tight_layout()
plt.show()

