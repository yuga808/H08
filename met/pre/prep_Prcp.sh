#!/bin/sh
############################################################
# Calculate daily precipitation: Rainf + Snowf
# Original: hanasaki, NIES
# Modified: ì˙éüèàóùëŒâûÅi2025Åj
############################################################

PRJ=ISS1
RUN=____
YEARMIN=2041
YEARMAX=2060

L=9331200
SUF=.gl5
#L=259200
#SUF=.hlf
#L=2247551
#SUF=.g5o

##########################
# Output directory
##########################
OUTDIR=../../met/dat/Prcp____
if [ ! -d $OUTDIR ]; then
  mkdir -p $OUTDIR
fi

##########################
# Loop over years, months, and days
##########################
YEAR=$YEARMIN
while [ $YEAR -le $YEARMAX ]; do
  for MON in 01 02 03 04 05 06 07 08 09 10 11 12; do
    DAY=01
    DAYMAX=`htcal $YEAR $MON`
    while [ $(expr $DAY + 0) -le $DAYMAX ]; do
      DAYSTR=`echo $DAY | awk '{printf("%02d", $1)}'`
      
      RAINF=../../met/dat/Rainf___/${PRJ}${RUN}${YEAR}${MON}${DAYSTR}${SUF}
      SNOWF=../../met/dat/Snowf___/${PRJ}${RUN}${YEAR}${MON}${DAYSTR}${SUF}
      PRCP=../../met/dat/Prcp____/${PRJ}${RUN}${YEAR}${MON}${DAYSTR}${SUF}
      
      echo "Processing: $PRCP"
      htmath $L add $RAINF $SNOWF $PRCP
      
      DAY=`expr $DAY + 1`
    done
  done
  YEAR=`expr $YEAR + 1`
done
