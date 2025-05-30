#!/bin/sh
############################################################
# Convert ISIMIP NetCDF to WFDEI-style binary daily files
# by 2025/02/19, takahashi (modified)
############################################################

#===========================#
# Settings (Change here)
#===========================#
YEARMIN=2041
YEARMAX=2041
L=259200               # 30-arcmin resolution: 720 x 360
XY="720 360"
TRESO=DY                # Temporal resolution: daily

# ISIMIP input vars
ISIMIP_VARS="rlds ps huss pr prsn rsds tas sfcwind"

# Mapping info (for htarray flipping)
L2X=../../map/dat/l2x_l2y_/l2x.hlf.txt
L2Y=../../map/dat/l2x_l2y_/l2y.hlf.txt

#===========================#
# Conversion Loop
#===========================#
for VAR in $ISIMIP_VARS; do

  # Map ISIMIP variable to WFDEI output name and output directory
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

  mkdir -p $DIROUT
  FILEIN=../../met/org/ISIMIP/mri-esm2-0_r1i1p1f1_w5e5_ssp370_${VAR}_global_daily_2041_2050.nc

  YEAR=$YEARMIN
  while [ $YEAR -le $YEARMAX ]; do
    echo "Processing $VAR ($VAR2) for $YEAR"

    TMPNC=tmp_${VAR}_${YEAR}.nc
    cdo selyear,$YEAR $FILEIN $TMPNC

    DAYS_IN_YEAR=$(cdo -s ntime $TMPNC | tr -d ' ')
    if [ -z "$DAYS_IN_YEAR" ]; then
      echo "Error: Failed to get number of days in $TMPNC"
      exit 1
    fi

    DAY_IDX=0
    while [ $DAY_IDX -lt $DAYS_IN_YEAR ]; do
      DAY_IDX=$((DAY_IDX + 1))

      # Extract specific day using seltimestep
      cdo -s seltimestep,$DAY_IDX $TMPNC tmp1.nc
      if [ ! -f tmp1.nc ]; then
        echo "Failed to extract timestep $DAY_IDX for $VAR $YEAR"
        continue
      fi

      OUTTXT=temp_${VAR}_${YEAR}_${DAY_IDX}.txt
      ncdump -v $VAR tmp1.nc | \
        sed -n '/data:/,/}/p' | \
        sed -e '1d' -e '$d' | \
        tr -d ',;=' | \
        tr -s ' ' '\n' | \
        awk '{if ($1 ~ /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/) printf("%s ", $1)}' | \
        sed 's/[[:space:]]*$//' > $OUTTXT
      echo >> $OUTTXT

      if [ ! -s "$OUTTXT" ]; then
        echo "Warning: $OUTTXT is empty. Skipping."
        continue
      fi

      ACTUAL=$(wc -w < "$OUTTXT")
      EXPECTED=259200
      if [ "$ACTUAL" -ne "$EXPECTED" ]; then
        echo "Warning: $OUTTXT has $ACTUAL values, expected $EXPECTED. Skipping."
        continue
      fi

      DATE=$(date -d "$YEAR-01-01 +$((DAY_IDX - 1)) days" +%Y%m%d)
      OUTFILE=${DIROUT}/isim____${DATE}.hlf

      prog_WFDEI $OUTTXT $YEAR ${DATE:4:2} 86400 $OUTFILE

      if [ -f $OUTFILE ]; then
        htarray $L $XY $L2X $L2Y upsidedown $OUTFILE $OUTFILE
      else
        echo "Warning: $OUTFILE not found, skipping htarray"
      fi
    done

    rm -f tmp1.nc $TMPNC
    YEAR=$((YEAR + 1))
  done

done

