import numpy as np
import os

def get_binary_shape(file_path, dtype=np.float32):
    size_bytes = os.path.getsize(file_path)
    num_elements = size_bytes // np.dtype(dtype).itemsize
    return num_elements

files = [
    '/home/kajiyama/H08/H08_20230612/lnd/out/Qtot____/W5E5LR__20190101.gl5',
    '../../lnd/out/Qtot____/ISIMLR__20410101.hlo',
    '../../lnd/out/AvgSurfT/ISIMLR__20410000.hlo',
    '../../map/out/riv_seq_/rivseq.WFDEI.hlo',
    '../../map/out/riv_nxl_/rivnxl.WFDEI.hlo',
    '../../map/out/riv_nxd_/rivnxd.WFDEI.hlo',
    '../../map/dat/lnd_ara_/lndara.WFDEI.hlo',
    '../../riv/dat/uniform.0.5.hlo',
    '../../riv/dat/uniform.1.4.hlo',
    '../../riv/ini/uniform.0.0.hlo',
    '../../met/dat/Prcp____/isim____00000000.hlo',
    '../../met/dat/Prcp____/isim____00000000.hlo',
    '../../lnd/dat/uniform.0.003.hlo',
    '../../lnd/dat/uniform.0.003.hlf',
    '../../map/dat/lnd_msk_/lndmsk.WFDEI.hlo',
    '../../lnd/dat/uniform.1.00.hlo',
    '../../lnd/dat/gamma___/isim____00000000.hlo',
    '../../map/dat/Albedo__/GSW2____.hloMM',
    '../../lnd/dat/gwr_____/fg.hlo',
    '../../lnd/out/SoilMois/ISIMLR__20410101.hlo'
]

for file in files:
    if os.path.exists(file):
        shape = get_binary_shape(file, np.float32)
        print(f"{file}: {shape} elements (float32)")
    else:
        print(f"{file}: not found")
