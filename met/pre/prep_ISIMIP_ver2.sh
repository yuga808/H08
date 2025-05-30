#!/bin/sh
############################################################
#to   prepare WATCH Forcing Data
#by   2025/02/19, takahashi
#Editting prep_WFDEI.sh for ISIMIP
############################################################
# Preparation
#
# 1) See ISIMIP's website and download netcdf files.
#
# 2) Make directory met/org/ISIMIP and put files as follows
# 
# met/org/ISIMIP/mri-esm2-0_r1l1p1f1_w5e5_...
#
# Please be careful about the size of downroaded data.
# (A decade in one file)
############################################################
# Settings (Change here)
############################################################
YEARMIN=2041
YEARMAX=2041
############################################################
# Macro (Do not change here unless you are an expert)
############################################################
DIRPWD=`pwd`
L=259200
MONS="01 02 03 04 05 06 07 08 09 10 11 12"
#VARS="LWdown PSurf Qair Rainf SWdown Snowf Tair Wind"
VARS="rlds ps huss prrn rsds prsn tas sfcwind"
TRESO=DY
############################################################
# Job (Convert netcdf file into binary file)
############################################################
for VAR in $VARS; do
  YEAR=$YEARMIN
  while [ $YEAR -le $YEARMAX ]; do
    for MON in $MONS; do
      if   [ $TRESO = DY ]; then
        SECINT=86400
      fi
# ISIMIP@to WFDEI
      BIGFILE=../../met/org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_${VAR}_global_daily_2041_2050.nc
      TMPFILE=tmp_${VAR}_${YEAR}${MON}.nc
      cdo selyear,${YEAR} -selmon,`echo ${MON} | sed 's/^0*//g'` $BIGFILE $TMPFILE
#
      if   [ $VAR = "rlds" ]; then
        DIROUT=../../met/dat/LWdown__
        VAR2=LWdown
      elif [ $VAR = "ps" ]; then
        DIROUT=../../met/dat/PSurf___
        VAR2=PSurf
      elif [ $VAR = "huss" ]; then
        DIROUT=../../met/dat/Qair____
        VAR2=Qair
      elif [ $VAR = "pr" ]; then
        DIROUT=../../met/dat/Rainf___
        VAR2=Rainf
      elif [ $VAR = "rsds" ]; then
        DIROUT=../../met/dat/SWdown__
        VAR2=SWdown
      elif [ $VAR = "prsn" ]; then
        DIROUT=../../met/dat/Snowf___
        VAR2=Snowf
      elif [ $VAR = "tas" ]; then
        DIROUT=../../met/dat/Tair____
        VAR2=Tair
      elif [ $VAR = "sfcwind" ]; then
        DIROUT=../../met/dat/Wind____
        VAR2=Wind
      fi

      if [ ! -d $DIROUT ]; then
        mkdir -p $DIROUT
      fi
      OUT=${DIROUT}/isim____.hlf

      NCHEAD=`ncdump -h $NC | wc | awk '{print $1}'`
      NCHEAD=`expr $NCHEAD + 2`
#
      ncdump -v$VAR $NC | sed '1,'${NCHEAD}'d' | sed -e '$d' | \
      sed -e 's/;//' | sed -e 's/,/ /g' | sed -e 's/_/1.0E20/g' > temp.txt
      prog_WFDEI temp.txt $YEAR $MON $SECINT ${OUT}${TRESO}
    done
    httime $L ${OUT}MO $YEAR $YEAR ${OUT}YR
    YEAR=`expr $YEAR + 1`
  done
done
