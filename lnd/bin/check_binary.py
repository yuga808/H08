import numpy as np

def read_binary(path, dtype=np.float32, count=-1):
    with open(path, 'rb') as f:
        return np.fromfile(f, dtype=dtype, count=count)
swe = read_binary('../../lnd/ini/uniform.0.0.g5o')
print('SWE min:', np.min(swe), 'max:', np.max(swe), 'nan:', np.isnan(swe).sum())
swdown = read_binary('../../met/dat/SWdown__/isim____.g5oDY')
print('SWDOWN min:', np.min(swdown), 'max:', np.max(swdown))

