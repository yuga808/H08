#!/bin/sh
############################################################
#to   calculate rainfall and snowfall from precipitation
#by   2010/01/31, hanasaki
############################################################
PRJ=isim
RUN=____
YEARMIN=2041
YEARMAX=2041
MONS="01 02 03 04 05 06 07 08 09 10 11 12"

#PRJ=AMeD           # for Kyusyu (.ks1)
#RUN=AS1_
#YEARMIN=2014
#YEARMAX=2014
#MONS="01 02 03 04 05 06 07 08 09 10 11 12"

#PRJ=AMeD           # for Kyusyu (.ks1)
#RUN=AS1_
#YEARMIN=2014
#YEARMAX=2014
#MONS="01 02 03 04 05 06 07 08 09 10 11 12"

############################################################
#
############################################################
L=2247551
SUF=.g5o

#L=32400      # for Kyusyu (.ks1)
#SUF=.ks1
#L=4032      # for Rio de Janeiro
#SUF=.rj5
#L=5184      # for Paris
#SUF=.pr5
#L=2304      # for Los Angeles
#SUF=.la5
#L=1296      # for Cape Town
#SUF=.ct5
#L=1728      # for Tokyo/London/Chennai
#SUF=.tk5
#SUF=.ln5
#SUF=.cn5
############################################################
#
############################################################
if [ ! -d ../../met/dat/Rainf___ ]; then
  mkdir   ../../met/dat/Rainf___
fi
if [ ! -d ../../met/dat/Snowf___ ]; then
  mkdir   ../../met/dat/Snowf___
fi
############################################################
#
############################################################
YEAR=$YEARMIN
while [ $YEAR -le $YEARMAX ]; do
  for MON in $MONS; do
    DAY=1
    DAYMAX=`htcal $YEAR $MON`
    while [ $DAY -le $DAYMAX ]; do
      DAY=`echo $DAY | awk '{printf("%2.2d",$1)}'`
       PRCP=../../met/dat/Prcp____/${PRJ}${RUN}${YEAR}${MON}${DAY}${SUF}
      PSURF=../../met/dat/PSurf___/${PRJ}${RUN}${YEAR}${MON}${DAY}${SUF}
       QAIR=../../met/dat/Qair____/${PRJ}${RUN}${YEAR}${MON}${DAY}${SUF}
       TAIR=../../met/dat/Tair____/${PRJ}${RUN}${YEAR}${MON}${DAY}${SUF}
      RAINF=../../met/dat/Rainf___/${PRJ}${RUN}${YEAR}${MON}${DAY}${SUF}
      SNOWF=../../met/dat/Snowf___/${PRJ}${RUN}${YEAR}${MON}${DAY}${SUF}
      htrs $L $PRCP $PSURF $QAIR $TAIR $RAINF $SNOWF
      DAY=`expr $DAY + 1`
    done
  done
  YEAR=`expr $YEAR + 1`
done
