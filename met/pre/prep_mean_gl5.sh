#!/bin/sh
######################################################
#to   prepare mean 
#by   2012/06/05, hanasaki
######################################################
# Geography (Edit here)
######################################################
L=9331200
SUF=.gl5
#L=2247551
#SUF=.g5o
######################################################
# Settings (Edit here)
######################################################
PRJ=isim
RUN=____
IDXORG=DY
YEARMIN=2051; YEARMAX=2060; YEAROUT=0000
######################################################
# Macro (Do not edit below unless you are an expert)
######################################################
DIR=/home/takahashi/H08/H08_20240718/met/dat
#SUBDIRS="Tair____ Qair____ PSurf___ Wind____ SWdown__ LWdown__ Snowf___ Prcp____ Rainf___"
SUBDIRS="Prcp____"
######################################################
# Job
######################################################
for SUBDIR in $SUBDIRS; do
  echo $SUBDIR
  IN=${DIR}/${SUBDIR}/${PRJ}${RUN}${SUF}
  httime $L ${IN}${IDXORG} $YEARMIN $YEARMAX ${IN}MO
#  httime $L ${IN}${IDXORG} $YEARMIN $YEARMAX ${IN}YR
  htmean $L ${IN}MO        $YEARMIN $YEARMAX $YEAROUT
  htmean $L ${IN}YR        $YEARMIN $YEARMAX $YEAROUT
done


