#!/bin/bash

echo Generating santa stats
${NF}/bin/V1_santa_stats.py ${OUT}/S4_santa && \

echo Generating santa bps
${NF}/bin/V2_santa_bp.py ${OUT}/S4_santa && \

echo Generating sim_bps for each RDM
Rscript ${NF}/bin/V3_sim_bp.R ${OUT}/V2_santa_bp.csv

