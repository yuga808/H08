def check_file_type(file_path):
    try:
        with open(file_path, 'r') as f:
            f.read(10000)
        return "ASCII (Text File)"
    except UnicodeDecodeError:
        return "Binary (Binary File)"

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
    result = check_file_type(file)
    print(f"{file}: {result}")
