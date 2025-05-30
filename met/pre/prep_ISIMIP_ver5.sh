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
YEARMAX=2050

############################################################
# Macro (Do not change here unless you are an expert)
############################################################
DIRPWD=`pwd`
L=259200
MONS="01 02 03 04 05 06 07 08 09 10 11 12"
VARS="rlds ps huss pr rsds prsn tas sfcwind"
TRESO=DY

############################################################
# Job (Convert netcdf file into binary file)
############################################################
for VAR in $VARS; do
  YEAR=$YEARMIN
  while [ $YEAR -le $YEARMAX ]; do
    for MON in $MONS; do
      if   [ $TRESO = 3H ]; then
        SECINT=10800
      elif [ $TRESO = DY ]; then
        SECINT=86400
      fi

      if   [ $VAR = "rlds" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/LWdown__
      elif [ $VAR = "ps" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/PSurf___
      elif [ $VAR = "huss" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/Qair____
      elif [ $VAR = "pr" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/Rainf___
      elif [ $VAR = "rsds" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/SWdown__
      elif [ $VAR = "prsn" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/Snowf___
      elif [ $VAR = "tas" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/Tair____
      elif [ $VAR = "sfcwind" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/Wind____
      fi

      if [ ! -d $DIROUT ]; then
        mkdir -p $DIROUT
      fi

      OUT=${DIROUT}/isim____.hlf
      NC=../../met/org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_${VAR}_global_daily_${YEARMIN}_${YEARMAX}.nc
      TMPNC=tmp_${VAR}_${YEAR}${MON}.nc
      cdo selyear,${YEAR} -selmon,${MON#0} $NC $TMPNC
      echo $TMPNC

      NCHEAD=`ncdump -h $TMPNC | wc -l`
      NCHEAD=`expr $NCHEAD + 2`

      ncdump -v$VAR $TMPNC | sed '1,'${NCHEAD}'d' | sed -e '$d' | \
        sed -e 's/;//' | sed -e 's/,/ /g' | sed -e 's/_/1.0E20/g' > temp.txt

      prog_WFDEI temp.txt $YEAR $MON $SECINT ${OUT}${TRESO}
      httime $L ${OUT}MO $YEAR $YEAR ${OUT}YR

      rm -f $TMPNC temp.txt
    done
    YEAR=`expr $YEAR + 1`
  done

done
