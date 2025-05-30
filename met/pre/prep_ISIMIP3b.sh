#!/bin/sh
############################################################
# to   prepare WATCH Forcing Data
# by   2025/04/15, takahashi
# Modified: Background execution & safe temp file handling
############################################################

# === SELF BACKGROUND EXECUTION ===
if [ "$1" != "--run" ]; then
  DATE=$(date +"%Y%m%d_%H%M%S")
  DIRLOG=../../met/log
  mkdir -p $DIRLOG
  LOGFILE=${DIRLOG}/prep_ISIMIP_$DATE.log
  echo "Running in background..."
  nohup "$0" --run > "$LOGFILE" 2>&1 &
  echo "Log: $LOGFILE"
  echo "Use: tail -f $LOGFILE"
  exit 0
fi

# === Settings ===
YEARMIN=2051
YEARMAX=2060
#YEARMIN=2011
#YEARMAX=2019
L=259200
MONS="01 02 03 04 05 06 07 08 09 10 11 12"
VARS="rlds ps huss pr rsds prsn tas sfcwind"
#VARS="rlds ps huss pr rsds prsn tas sfcwind"
TRESO=DY
SECINT=86400  # Only DY supported

# === Job ===
for VAR in $VARS; do
  YEAR=$YEARMIN
  while [ $YEAR -le $YEARMAX ]; do
    for MON in $MONS; do

      # Output dir decision
      case $VAR in
        rlds)     DIROUT=../../met/dat/LWdown__ ;;
        ps)       DIROUT=../../met/dat/PSurf___ ;;
        huss)     DIROUT=../../met/dat/Qair____ ;;
        pr)       DIROUT=../../met/dat/Rainf___ ;;
        rsds)     DIROUT=../../met/dat/SWdown__ ;;
        prsn)     DIROUT=../../met/dat/Snowf___ ;;
        tas)      DIROUT=../../met/dat/Tair____ ;;
        sfcwind)  DIROUT=../../met/dat/Wind____ ;;
      esac

      mkdir -p $DIROUT

#      OUT=${DIROUT}/isim____.hlf
#      NC=../../met/org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_${VAR}_global_daily_${YEARMIN}_${YEARMAX}.nc
      OUT=${DIROUT}/ISS1____.hlf
      NC=../../met/org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp126_${VAR}_global_daily_${YEARMIN}_${YEARMAX}.nc
#      OUT=${DIROUT}/W5E5____.hlf
#      NC=/work/common/H08/met_data/W5E5v2.0_Lang_2021/${VAR}_W5E5v2.0_${YEARMIN}0101-${YEARMAX}1231.nc
      TMPNC=tmp_${VAR}_${YEAR}${MON}.nc
      TMPTXT=tmp_${VAR}_${YEAR}${MON}.txt

      echo "Processing $TMPNC"

      cdo selyear,${YEAR} -selmon,${MON#0} $NC $TMPNC

      NCHEAD=$(ncdump -h $TMPNC | wc -l)
      NCHEAD=$((NCHEAD + 2))

      ncdump -v$VAR $TMPNC | \
        sed "1,${NCHEAD}d" | sed -e '$d' | \
        sed -e 's/;//' -e 's/,/ /g' -e 's/_/1.0E20/g' > $TMPTXT

      prog_WFDEI $TMPTXT $YEAR $MON $SECINT ${OUT}${TRESO}
      
# takahashi Add upside-down flip using htarray
#     htarray $L "720 360" ../../map/dat/l2x_l2y_/l2x.hlf.txt ../../map/dat/l2x_l2y_/l2y.hlf.txt upsidedown ${OUT}${TRESO} ${OUT}${TRESO}
      
      httime $L ${OUT}MO $YEAR $YEAR ${OUT}YR

      rm -f $TMPNC $TMPTXT
    done
    YEAR=$((YEAR + 1))
  done
done
