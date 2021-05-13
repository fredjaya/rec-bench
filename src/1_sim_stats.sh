#!/bin/bash

echo Generating santa stats
${NF}/bin/V1_santa_stats.py ${OUT}/S4_santa && \

echo Generating santa bps
${NF}/bin/V2_santa_bp.py ${OUT}/S4_santa && \

echo Generating sim_bps for each RDM
Rscript ${NF}/bin/V3_sim_bp.R ${OUT}/V2_santa_bp.csv && \

echo Calculating pairwise distances
for fa in ${OUT}/S4_santa/*.fasta; do
	echo -n ${fa}', ' >> ${OUT}/V4_sim_distances.csv
	dist=$(Rscript ${NF}/bin/V4_sim_distances.R ${fa} | \
		sed 's/"//g' | sed 's/\[1\]//g')  
	echo $dist >> ${OUT}/V4_sim_distances.csv
done

echo Counting breakpoints
${NF}/bin/V5_fasta_to_bpcounts.py ${OUT}/S4_santa
