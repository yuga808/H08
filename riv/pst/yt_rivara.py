import numpy as np

infile = '../../map/out/riv_ara_/rivara.CAMA.gl5'
maskfile = '../../map/dat/lnd_msk_/lndmsk.CAMA.gl5'
outfile = '../../map/out/riv_ara_/rivara.CAMA.gl5.masked'

# load data
data = np.fromfile(infile, dtype='float32')
mask = np.fromfile(maskfile, dtype='float32')

# check size
assert data.shape[0] == mask.shape[0] == 9331200

# only keep land values, mask out sea (even if sea has 1e20 etc)
data[mask < 0.5] = 0.0

# save
data.astype('float32').tofile(outfile)
print(f"[OK] Masked file written: {outfile}")
