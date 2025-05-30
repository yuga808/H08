import numpy as np

# === 設定 ===
LDBG = 1  # チェックしたいデバッグポイント（Fortranは1始まり）

# === ファイルパス（適宜修正してください）===
mask = np.fromfile("../../map/dat/lnd_msk_/lndmsk.CAMA.g5o", dtype=np.float32)
val = mask[LDBG - 1]
print(f"LDBG={LDBG}, 値={val}")

if np.isclose(val, 1.0):
    print("✅ このセルは陸域（有効セル）です")
elif np.isclose(val, 0.0):
    print("⚠️ このセルは海域（無効セル）です")
else:
    print("⚠️ このセルは欠損または異常値です")
    
import numpy as np

data = np.fromfile("../../map/dat/lnd_msk_/lndmsk.CAMA.g5o", dtype=np.int32)
target = 1
matches = np.where(data == target)[0]

if len(matches) > 0:
    for match in matches:
        print(f"gl5 index {target} is at g5o index {match + 1}")
else:
    print(f"gl5 index {target} not found in g5o")

