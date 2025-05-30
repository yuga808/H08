## -*- coding: utf-8 -*-
#
#import numpy as np
#from collections import defaultdict
#
## ��: riv_num.g5o�iint32�j�Atemp.lndbal.g5o�ifloat32�j���o�C�i���œǂ�
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
## �S����̍��v�l�E��
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
## ��0����ID�������o���ď����o��
#with open("nonzero_basins.txt", "w") as f:
#    for rid in sorted(bal_sum.keys()):
#        if bal_sum[rid] != 0:
#            f.write(f"{rid}\t{bal_sum[rid]:.6f}\t{bal_count[rid]}\n")
#            # print(f"Basin {rid}: sum = {bal_sum[rid]:.6f}, count = {bal_count[rid]}")  # ��ʕ\�����������ꍇ
            
# -*- coding: utf-8 -*-

import numpy as np
from collections import defaultdict

# ===== �t�@�C���Ǎ� =====
# ����ID�}�b�v�ifloat32/big-endian�ŕۑ�����Ă��Ȃ��ꍇ�͓K�X�C���j
riv_num = np.fromfile("../../map/out/riv_num_/rivnum.CAMA.g5o", dtype=np.float32)
# �����x�o�����X�}�b�v
lndbal = np.fromfile('temp.lndbal.g5o', dtype='>f4')
# �e�i�q�̖ʐ�[km^2]
area = np.fromfile("../../map/dat/lnd_ara_/lndara.CAMA.g5o", dtype=np.float32)

# ===== ���悲�Ƃ�BALLND�i�̐ω��d�a�j�W�v =====
bal_sum = defaultdict(float)
bal_count = defaultdict(int)

for rid, bal, a in zip(riv_num, lndbal, area):
    bal_sum[rid] += bal * a    # [mm] �~ [km^2] �� mm�Ekm^2
    bal_count[rid] += 1

# mm�Ekm^2 �� km^3/�N�ɕϊ��i1mm=1e-6km�Akm^2���̂܂܂Ȃ̂Ł�1e6��km^3�j
for rid in bal_sum:
    bal_sum[rid] /= 1e6        # [km^3/�N]

# ===== �o�́E�t�@�C���ۑ� =====

# �S������̕\���Ɣ�0�̂݃t�@�C���o��
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
