import os

files = [
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
    '../../lnd/dat/uniform.0.003.hlf'
]

for file in files:
    if os.path.exists(file):
        with open(file, 'rb') as f:
            lines = sum(1 for line in f)
        print(f"{file}: {lines} lines (binary mode)")
    else:
        print(f"{file}: not found")
