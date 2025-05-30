## -*- coding: utf-8 -*-
#
#import numpy as np
#from collections import defaultdict
#
## 例: riv_num.g5o（int32）、temp.lndbal.g5o（float32）をバイナリで読む
#riv_num = np.fromfile("../../map/out/riv_num_/rivnum.CAMA.g5o", dtype=np.float32)
#lndbal = np.fromfile('temp.lndbal.g5o', dtype='>f4')
#
#bal_sum = defaultdict(float)
#bal_count = defaultdict(int)
#
#for rid, bal in zip(riv_num, lndbal):
#    bal_sum[rid] += bal
#    bal_count[rid] += 1
#
## 全流域の合計値・個数
#total_sum = 0.0
#total_count = 0
#nonzero_basins = 0
#
#for rid in sorted(bal_sum.keys()):
#    print(f"Basin {rid}: sum = {bal_sum[rid]:.6f}, count = {bal_count[rid]}")
#    total_sum += bal_sum[rid]
#    total_count += bal_count[rid]
#    if bal_sum[rid] != 0:
#        nonzero_basins += 1
#
#print(f"num of ID: {len(bal_sum)}")
#print(f"total: {total_count}")
#print(f"sum: {total_sum:.6f}")
#print(f"nonzero: {nonzero_basins}")
#
#for rid, bal in zip(riv_num, lndbal):
#    bal_sum[rid] += bal
#    bal_count[rid] += 1
#
## 非0流域IDだけ抽出して書き出す
#with open("nonzero_basins.txt", "w") as f:
#    for rid in sorted(bal_sum.keys()):
#        if bal_sum[rid] != 0:
#            f.write(f"{rid}\t{bal_sum[rid]:.6f}\t{bal_count[rid]}\n")
#            # print(f"Basin {rid}: sum = {bal_sum[rid]:.6f}, count = {bal_count[rid]}")  # 画面表示もしたい場合
            
# -*- coding: utf-8 -*-

import numpy as np
from collections import defaultdict

# ===== ファイル読込 =====
# 流域IDマップ（float32/big-endianで保存されていない場合は適宜修正）
riv_num = np.fromfile("../../map/out/riv_num_/rivnum.CAMA.g5o", dtype=np.float32)
# 水収支バランスマップ
lndbal = np.fromfile('temp.lndbal.g5o', dtype='>f4')
# 各格子の面積[km^2]
area = np.fromfile("../../map/dat/lnd_ara_/lndara.CAMA.g5o", dtype=np.float32)

# ===== 流域ごとのBALLND（体積加重和）集計 =====
bal_sum = defaultdict(float)
bal_count = defaultdict(int)

for rid, bal, a in zip(riv_num, lndbal, area):
    bal_sum[rid] += bal * a    # [mm] × [km^2] → mm・km^2
    bal_count[rid] += 1

# mm・km^2 → km^3/年に変換（1mm=1e-6km、km^2そのままなので÷1e6でkm^3）
for rid in bal_sum:
    bal_sum[rid] /= 1e6        # [km^3/年]

# ===== 出力・ファイル保存 =====

# 全流域情報の表示と非0のみファイル出力
total_sum = 0.0
nonzero_basins = 0

with open("nonzero_basins_ballnd.txt", "w") as f:
    for rid in sorted(bal_sum.keys()):
        ballnd = bal_sum[rid]
        count = bal_count[rid]
        print(f"Basin {int(rid)}: BALLND = {ballnd:.6f} km^3/y, count = {count}")
        total_sum += ballnd
        if ballnd > 0.00001:
            nonzero_basins += 1
            f.write(f"{int(rid)}\t{ballnd:.6f}\t{count}\n")

print(f"bal_sum: {len(bal_sum)}")
print(f"total_sum: {total_sum:.6f} km^3/y")
print(f"nonzero_basins: {nonzero_basins}")
print("saved")
