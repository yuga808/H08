#!/bin/sh
############################################################
# to   prepare WATCH Forcing Data
# by   2025/02/19, takahashi
# Editting prep_WFDEI.sh for ISIMIP
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
  # sfcwind only
  if [ "$VAR" != "sfcwind" ]; then
    continue
  fi

  YEAR=$YEARMIN
  while [ $YEAR -le $YEARMAX ]; do
    # after 2047
    if [ $YEAR -lt 2047 ]; then
      YEAR=`expr $YEAR + 1`
      continue
    fi

    for MON in $MONS; do
      if [ $TRESO = DY ]; then
        SECINT=86400
      fi

      ADD=ISIMIP
      DIROUT=../../met/dat/Wind____
      [ ! -d "$DIROUT" ] && mkdir -p "$DIROUT"

      OUT=${DIROUT}/isim____.hlf
      NC=../../met/org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_${VAR}_global_daily_${YEARMIN}_${YEARMAX}.nc
      TMPNC=tmp_${VAR}_${YEAR}${MON}.nc
      cdo selyear,${YEAR} -selmon,${MON#0} $NC $TMPNC
      echo "Processing: $TMPNC"

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

