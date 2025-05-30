# -*- coding: utf-8 -*-
import numpy as np

YEAR     = 2060         # �Ώ۔N
YEARMIN  = YEAR - 1     # ������Ԃ̔N�i�O�N12���j
YEARMAX  = YEAR         # �I����Ԃ̔N�i���N12���j
SUF      = "g5o"        # �t�@�C���g���q�i��: gl5, g5o�j
PRJMET   = "isim"
PRJ      = "ISIM"

# === �萔 ===
DAYS = 365
SECONDS_PER_DAY = 86400
KG_TO_KM3 = 1e-12

# === �t�@�C���ǂݍ��݊֐� ===
def load_file(path, dtype=np.float32):
    try:
        return np.fromfile(path, dtype=dtype)
    except:
        print(f"[missing] {path}")
        return None


# === ���ʃp�X�ݒ� ===
base_map = "../../map/dat"
base_met = "../../met/dat"
base_lnd = "../../lnd/out"
base_riv = "../../riv/out"
base_map_out = "../../map/out"

#base_map = "/home/kajiyama/H08/H08_20230612/map/dat"
#base_met = "/home/kajiyama/H08/H08_20230612/met/dat"
#base_lnd = "/home/kajiyama/H08/H08_20230612/lnd/out"
#base_riv = "/home/kajiyama/H08/H08_20230612/riv/out"
#base_map_out = "/home/kajiyama/H08/H08_20230612/map/out"

# === �ʐςƃ}�X�N ===
area = load_file(f"{base_map}/lnd_ara_/lndara.CAMA.{SUF}")
mask = load_file(f"{base_map}/lnd_msk_/lndmsk.CAMA.{SUF}").astype(int)

valid = (mask == 1) & (area > 0) & np.isfinite(area)

# === �C�ہE���ʃ��f���o�� ===
rainf    = load_file(f"{base_met}/Rainf___/{PRJMET}____{YEAR}0000.{SUF}")
snowf    = load_file(f"{base_met}/Snowf___/{PRJMET}____{YEAR}0000.{SUF}")
evap     = load_file(f"{base_lnd}/Evap____/{PRJ}LR__{YEAR}0000.{SUF}")
qtot     = load_file(f"{base_lnd}/Qtot____/{PRJ}LR__{YEAR}0000.{SUF}")
soil_ini = load_file(f"{base_lnd}/SoilMois/{PRJ}LR__{YEARMIN}1200.{SUF}")
soil_end = load_file(f"{base_lnd}/SoilMois/{PRJ}LR__{YEARMAX}1200.{SUF}")
swe_ini  = load_file(f"{base_lnd}/SWE_____/{PRJ}LR__{YEARMIN}1200.{SUF}")
swe_end  = load_file(f"{base_lnd}/SWE_____/{PRJ}LR__{YEARMAX}1200.{SUF}")
gw_ini   = load_file(f"{base_lnd}/GW______/{PRJ}LR__{YEARMIN}1200.{SUF}")
gw_end   = load_file(f"{base_lnd}/GW______/{PRJ}LR__{YEARMAX}1200.{SUF}")

# === �ʐςƃ}�X�N ===
#area = load_file("/home/kajiyama/H08/H08_20230612/map/dat/lnd_ara_/lndara.CAMA.gl5")  # [km2]
#mask = load_file("/home/kajiyama/H08/H08_20230612/map/dat/lnd_msk_/lndmsk.CAMA.gl5").astype(int)  # 1=��, 0=�C
#
#valid = (mask == 1) & (area > 0) & np.isfinite(area)
#
#rainf = load_file("/home/kajiyama/H08/H08_20230612/met/dat/Rainf___/W5E5____20190000.gl5")
#snowf = load_file("/home/kajiyama/H08/H08_20230612/met/dat/Snowf___/W5E5____20190000.gl5")
#evap  = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/Evap____/W5E5LR__20190000.gl5")
#qtot  = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/Qtot____/W5E5LR__20190000.gl5")
#soil_ini = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/SoilMois/W5E5LR__20181200.gl5")
#soil_end = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/SoilMois/W5E5LR__20191200.gl5")
#swe_ini  = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/SWE_____/W5E5LR__20181200.gl5")
#swe_end  = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/SWE_____/W5E5LR__20191200.gl5")
#gw_ini   = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/GW______/W5E5LR__20181200.gl5")
#gw_end   = load_file("/home/kajiyama/H08/H08_20230612/lnd/out/GW______/W5E5LR__20191200.gl5")


# === �v�Z�֐� ===
def flux_to_km3(data, name):
    if data is None:
        print(f"{name:<8}: missing")
        return 0.0
    flux = data[valid]
    km3 = np.sum(flux * SECONDS_PER_DAY * DAYS * area[valid]) * KG_TO_KM3
    print(f"{name:<8}: {km3:12.6f} km3/y")
    return km3

def delta_to_km3(data1, data2, name):
    if data1 is None or data2 is None:
        print(f"{name:<8}: missing")
        return 0.0
    delta = data2[valid] - data1[valid]
    km3 = np.sum(delta * area[valid]) * KG_TO_KM3
    print(f"{name:<8}: {km3:12.6f} km3/y")
    return km3

rainf_km3 = flux_to_km3(rainf, "RAINF")
snowf_km3 = flux_to_km3(snowf, "SNOWF")
prcp_km3 = rainf_km3 + snowf_km3
print(f"{'PRCP':<8}: {prcp_km3:12.6f} km3/y")  # �� ���Z�l��PRCP�Ƃ��ĕ\��

evap_km3 = flux_to_km3(evap, "EVAP")
qtot_km3 = flux_to_km3(qtot, "QTOT")
delsm_km3 = delta_to_km3(soil_ini, soil_end, "DELSM")
delswe_km3 = delta_to_km3(swe_ini, swe_end, "DELSWE")
delgw_km3 = delta_to_km3(gw_ini, gw_end, "DELGW")

# === BALLND �v�Z ===
ballnd_km3 = prcp_km3 - evap_km3 - qtot_km3 - delsm_km3 - delswe_km3 - delgw_km3
print(f"\n[BALLND] Water balance of land: {ballnd_km3:.6f} km3/y")

# === FBALLND�v�Z�p valid�i�}�X�N�Ȃ��Aarea�L���̂݁j ===
valid_all = (area > 0) & np.isfinite(area)

def flux_to_km3_all(data, name):
    if data is None:
        print(f"{name:<8} (ALL): missing")
        return 0.0
    flux = data[valid_all]
    km3 = np.sum(flux * SECONDS_PER_DAY * DAYS * area[valid_all]) * KG_TO_KM3
    print(f"{name:<8} (ALL): {km3:12.6f} km3/y")
    return km3

def delta_to_km3_all(data1, data2, name):
    if data1 is None or data2 is None:
        print(f"{name:<8} (ALL): missing")
        return 0.0
    delta = data2[valid_all] - data1[valid_all]
    km3 = np.sum(delta * area[valid_all]) * KG_TO_KM3
    print(f"{name:<8} (ALL): {km3:12.6f} km3/y")
    return km3

# === FBALLND�̍\���imask���g��Ȃ��j ===
prcp_fballnd = flux_to_km3_all(rainf, "RAINF") + flux_to_km3_all(snowf, "SNOWF")
evap_fballnd = flux_to_km3_all(evap, "EVAP")
qtot_fballnd = flux_to_km3_all(qtot, "QTOT")
delsm_fballnd = delta_to_km3_all(soil_ini, soil_end, "DELSM")
delswe_fballnd = delta_to_km3_all(swe_ini, swe_end, "DELSWE")
delgw_fballnd = delta_to_km3_all(gw_ini, gw_end, "DELGW")

fballnd_km3 = prcp_fballnd - evap_fballnd - qtot_fballnd - delsm_fballnd - delswe_fballnd - delgw_fballnd
print(f"\n[FBALLND] Global water balance (all land): {fballnd_km3:.6f} km3/y")
#
# === BALRIV �v�Z�ǉ��i�R�[�h�����ɂ��̂܂ܓ\��t���Ă��������j ===

# �t�@�C���ǂݍ���
rivout = load_file("../../riv/out/riv_out_/ISIMLR__{YEAR}0000.g5o")
rivsto_ini = load_file("../../riv/out/riv_sto_/ISIMLR__{YEARMIN}1200.g5o")
rivsto_end = load_file("../../riv/out/riv_sto_/ISIMLR__{YEARMAX}1200.g5o")
rivmou = load_file("../../map/out/riv_mou_/rivmou.CAMA.g5o")


#rivout = load_file("/home/kajiyama/H08/H08_20230612/riv/out/riv_out_/W5E5LR__20190000.gl5")
#rivsto_ini = load_file("/home/kajiyama/H08/H08_20230612/riv/out/riv_sto_/W5E5LR__20181200.gl5")
#rivsto_end = load_file("/home/kajiyama/H08/H08_20230612/riv/out/riv_sto_/W5E5LR__20191200.gl5")
#rivmou = load_file("/home/kajiyama/H08/H08_20230612/map/out/riv_mou_/rivmou.CAMA.gl5")


#print("area size         :", area.shape if area is not None else "None")
#print("mask unique values:", np.unique(mask) if mask is not None else "None")
#print("rivmou unique     :", np.unique(rivmou)[:10] if rivmou is not None else "None")

# �g�ݍ��킹�̊m�F
if mask is not None and rivmou is not None:
    cond_both = (mask == 1) & (rivmou == 9)
    print("rivmou == 9 count:", np.sum(rivmou == 9))
    print("mask == 1 count  :", np.sum(mask == 1))
    print("rivmou==9 & mask==1:", np.sum(cond_both))


# �L���i�q�����imask == 1 ���� rivmou == 9�j
valid_rivout = (mask == 1) & (rivmou == 9) & (area > 0) & np.isfinite(area)
#valid_rivout = (rivmou == 9) & (area > 0) & np.isfinite(area) & np.isfinite(rivout)

# RIVOUT�i���o�ʁj
rivout_km3 = (
    np.sum(rivout[valid_rivout]) * SECONDS_PER_DAY * DAYS * KG_TO_KM3
    if rivout is not None else 0.0
)


# DELRIVSTO�i�����ʂ̍����j
delrivsto_km3 = (
    np.sum(rivsto_end[valid] - rivsto_ini[valid]) * KG_TO_KM3
    if rivsto_ini is not None and rivsto_end is not None else 0.0
)

# BALRIV �v�Z�iQTOT �͊��� ballnd_km3 �v�Z�Ɏg���Ă���l�j
balriv_km3 = qtot_km3 - rivout_km3 - delrivsto_km3

# �o��
print("\n=== River Balance Summary (BALRIV) ===")
print(f"QTOT      : {qtot_km3:12.6f} km3/y")
print(f"RIVOUT    : {rivout_km3:12.6f} km3/y")
print(f"DELRIVSTO : {delrivsto_km3:12.6f} km3/y")
print(f"BALRIV    : {balriv_km3:12.6f} km3/y")




