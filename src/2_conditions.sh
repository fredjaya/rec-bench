#!/bin/bash

echo Calculating Profile conditions
${NF}/bin/F1_addCondition_phiProfile.py V3_profile_sim_bp.csv ${OUT}/B1_phi_profile && \

echo Calculating 3SEQ conditions
${NF}/bin/F2_addCondition_3SEQ.py V3_3seq_sim_bp.csv ${OUT}/B2_3seq && \

echo Concatenating GENECONV outputs
${NF}/bin/F3_concat_gc_outputs.py ${OUT}/B3_geneconv && \

echo Separating sequence pairs
Rscript ${NF}/bin/F3_separate_seq_pairs.R ${OUT}/F3_geneconv_summarised.csv && \

echo Calculating GENECONV conditions
${NF}/bin/F3_addCondition_geneconv2.py ${OUT}/V3_gc_sim_bp.csv ${OUT}/F3_geneconv_unpaired.csv && \
