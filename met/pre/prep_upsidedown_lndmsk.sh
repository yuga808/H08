#!/bin/bash
############################################################
# Flip lndmsk upside-down
# Author: takahashi
# Date: 2025/04/11
############################################################

# ファイル情報（必要に応じて修正）
PRJ=GSW2
MAP=.CAMA
SUF=.gl5
VAR=lndmsk
L=9331200
XY="4320 2160"
L2X=../../map/dat/l2x_l2y_/l2x.gl5.txt
L2Y=../../map/dat/l2x_l2y_/l2y.gl5.txt

# 入出力ファイル
INFILE=../../map/dat/lnd_msk_/${VAR}${MAP}${SUF}
OUTFILE=../../map/dat/lnd_msk_/${VAR}${MAP}${SUF}

# 処理実行
echo "Flipping $INFILE -> $OUTFILE"
htarray $L $XY $L2X $L2Y upsidedown $INFILE $OUTFILE

