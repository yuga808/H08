# 2024/03/12 by kajiyama

import numpy as np

# Setting
nx=4320
ny=2160
n0ord=2 # maximum count of origin grids to same destination

# Input
aq1 = np.fromfile(f'../../../map/org/Aoba/existing_destination_1.gl5','float32').reshape(ny,nx)
aq2 = np.fromfile(f'../../../map/org/Aoba/existing_destination_2.gl5','float32').reshape(ny,nx)
aq3 = np.fromfile(f'../../../map/org/Aoba/existing_destination_3.gl5','float32').reshape(ny,nx)
aq4 = np.fromfile(f'../../../map/org/Aoba/existing_destination_4.gl5','float32').reshape(ny,nx)

# save array
out = np.full((n0ord,ny,nx), 1e+20)

# destination canal id
for a in range(ny):
    for b in range(nx):
        if n0ord >= 1 and aq1[a,b] > 0:
            print(aq1[a,b])
            out[0,a,b] = aq1[a,b]
        if n0ord >= 2 and aq2[a,b] > 0:
            print(aq2[a,b])
            out[1,a,b] = aq2[a,b]
        if n0ord >= 3 and aq3[a,b] > 0:
            print(aq3[a,b])
            out[2,a,b] = aq3[a,b]
        if n0ord >= 4 and aq4[a,b] > 0:
            print(aq4[a,b])
            out[3,a,b] = aq4[a,b]

# output
out.astype(np.float32).tofile(f'../../../map/org/Aoba/explicit_destination.bin')
