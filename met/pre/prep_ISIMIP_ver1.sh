#!/bin/sh
############################################################
#to   prepare WATCH Forcing Data
#by   2024/12/13, takahashi
#Editting prep_WFDEI.sh for ISIMIP
############################################################
# Preparation
#
# 1) See WFDEI's website and download netcdf files.
#
# 2) Make directory met/org/WFDEI and put files as follows
# 
# met/org/WFDEI/daily/Tair_daily_WFDEI_${YEAR}${MON}.nc
# met/org/WFDEI/daily/Qair_daily_WFDEI_${YEAR}${MON}.nc
# met/org/WFDEI/daily/Wind_daily_WFDEI_${YEAR}${MON}.nc
# met/org/WFDEI/daily/PSurf_daily_WFDEI_${YEAR}${MON}.nc
# met/org/WFDEI/daily/Rainf_daily_WFDEI_CRU_${YEAR}${MON}.nc
# met/org/WFDEI/daily/Snowf_daily_WFDEI_CRU_${YEAR}${MON}.nc
# met/org/WFDEI/daily/LWdown_daily_WFDEI_${YEAR}${MON}.nc
# met/org/WFDEI/daily/SWdown_daily_WFDEI_${YEAR}${MON}.nc
#
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
#      if   [ $VAR = "LWdown" ]; then(outdated)
      if   [ $VAR = "rlds" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/LWdown__
	VAR2=LWdown
#      elif [ $VAR = "PSurf" ]; then(outdated)
       elif [ $VAR = "ps" ]; then
        ADD=ISIMIP
        DIROUT=../../met/dat/PSurf___
	VAR2=PSurf
#      elif [ $VAR = "Qair" ]; then(outdated)
       elif [ $VAR = "huss" ]; then
	ADD=ISIMIP
        DIROUT=../../met/dat/Qair____
	VAR2=Qair
#      elif [ $VAR = "Rainf" ]; then(outdated)
       elif [ $VAR = "pr" ] ; then
#	ADD=WFDEI_CRU(outdated)
	ADD=ISIMIP  
        DIROUT=../../met/dat/Rainf___
	VAR2=Rainf
#      elif [ $VAR = "SWdown" ]; then(outdated)
       elif [ $VAR = "rsds" ]; then
	ADD=ISIMIP
        DIROUT=../../met/dat/SWdown__
	VAR2=SWdown
#      elif [ $VAR = "Snowf" ]; then(outdated)
       elif [ $VAR = "prsn" ]; then
#	ADD=WFDEI_CRU(outdated)
        ADD=ISIMIP
	DIROUT=../../met/dat/Snowf___
	VAR2=Snowf
#      elif [ $VAR = "Tair" ]; then(outdated)
       elif [ $VAR = "tas" ]; then
	ADD=ISIMIP
        DIROUT=../../met/dat/Tair____
	VAR2=Tair
#      elif [ $VAR = "Wind" ]; then(outdated)
       elif [ $VAR = "sfcwind" ]; then
	ADD=ISIMIP
        DIROUT=../../met/dat/Wind____
	VAR2=Wind
      fi
      if [ ! -d $DIROUT ]; then
        mkdir -p $DIROUT
      fi
      OUT=${DIROUT}/isim____.hlf
#
      if   [ $TRESO = 3H ]; then
#  NC=../../met/org/WFDEI/3hourly/${VAR}_${ADD}_${YEAR}${MON}.nc(outdated)
      NC=../../met/org/WFDEI/3hourly/${VAR2}_${ADD}_${YEAR}${MON}.nc
      elif [ $TRESO = DY ]; then
#  NC=../../met/org/WFDEI/daily/${VAR}_daily_${ADD}_${YEAR}${MON}.nc(outdated)
      BIGFILE=../../met/org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_${VAR}_global_daily_2041_2050.nc
      TMPFILE=tmp_${VAR}_${YEAR}${MON}.nc
      cdo selyear,${YEAR} -selmon,`echo ${MON} | sed 's/^0*//g'` $BIGFILE $TMPFILE
      fi
      NC=$TMPFILE
      echo "Processing: $NC"
#
      NCHEAD=`ncdump -h $NC | wc | awk '{print $1}'`
      NCHEAD=`expr $NCHEAD + 2`
#
      ncdump -v$VAR $NC | sed '1,'${NCHEAD}'d' | sed -e '$d' | \
      sed -e 's/;//' | sed -e 's/,/ /g' | sed -e 's/_/1.0E20/g' > temp.txt
      prog_WFDEI temp.txt $YEAR $MON $SECINT ${OUT}${TRESO}
      rm -f $TMPFILE
    done
    httime $L ${OUT}MO $YEAR $YEAR ${OUT}YR
    YEAR=`expr $YEAR + 1`
  done
done

