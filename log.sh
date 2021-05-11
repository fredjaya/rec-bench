# Making a note of all scripts required:
#V1_santa_stats.py 
#V2_santa_bp.py 
#V3_sim_bp.R 
#F1_addCondition_phiProfile.py
#F2_addCondition_3SEQ.py
#F3_concat_gc_outputs.py
#F3_separate_seq_pairs.R
#F3_addCondition_geneconv2.py

###################
### Simulations ###
###################

# Git: dba966f94174019b410e5c8330a0b11bca8c3e66

### Generate new simulated dataset where:
# 1. 99 generations of mutation only (m = 0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3)
# 2. 1 generation of recombination only (r = 0, 0.001, 0.005, 0.01, 0.05, 0.1; d = 0, 1)
# and all files process by all five RDMs

# Set env variables (UTS HPCC)
mkdir -p /shared/homes/13444841/2104_pub
export OUT=/shared/homes/13444841/2104_pub
export NF=/shared/homes/13444841/rec-bench
cd $OUT

nextflow run ${NF}/sim.nf \
	--seq ${NF}/data/FP7_patient_037_allseqs.fasta \
	--xml ${NF}/data/neutral.xml \
	--out ${OUT}

#######################################
### Simulation stats and conditions ###
#######################################

# Git: a899ddd63a78408c762a9cf6552583d1ebbfae75

# Activate conda environment 
# conda env create --file ${NF}/environment.yml
conda activate fredjaya-rec-bench-0.1.0

# Generate simulation statistics
${NF}/src/1_sim_stats.sh

# Calculate conditions
${NF}/src/2_conditions.sh

###################
### Scalability ###
###################

# Git:

# Set env variables (UTS HPCC)
mkdir -p /shared/homes/13444841/2104_scale
export OUT=/shared/homes/13444841/2104_scale
export NF=/shared/homes/13444841/rec-bench
cd $OUT

nextflow run ${NF}/sim.nf \
	--mode scalability \
	--seq ${NF}/data/FP7_patient_037_allseqs.fasta \
	--xml ${NF}/data/neutral.xml \
	--out ${OUT}
