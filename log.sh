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

# Git: e43781f756f9fc6d576c296228c0b9c4e40e057f

### Generate new simulated dataset where:
# 1. 99 generations of mutation only (m = 0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3)
# 2. 1 generation of recombination only (r = 0, 0.001, 0.005, 0.01, 0.05, 0.1; d = 0, 1)
# and all files process by all five RDMs

# Set env variables (UTS HPCC)
mkdir -p /shared/homes/13444841/2104_performance
export OUT=/shared/homes/13444841/2104_performance
export NF=/shared/homes/13444841/rec-bench
cd $OUT
# May need to run the following to fix matplotlib qt error
# export QT_QPA_PLATFORM='offscreen'

nextflow run ${NF}/sim.nf \
	--mode performance \
	--seq ${NF}/data/FP7_patient_037_allseqs.fasta \
	--xml ${NF}/data/neutral.xml \
	--out ${OUT}

########################
### Simulation stats ###
########################

# Git: e43781f756f9fc6d576c296228c0b9c4e40e057f

# Activate conda environment 
# conda env create --file ${NF}/environment.yml
conda activate fredjaya-rec-bench-0.1.0

# Generate simulation statistics
${NF}/src/1_sim_stats.sh

###################
### Scalability ###
###################

# Git: 43d8c5202de5517375a476420c4f744b4d38c9ad

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

# Been manually changing seqnum = Channel.from(n) with n and running each n
# separately.

# At n = 10000, no GENECONV runs finished. 60 = timed out, 10 = too similar
# Not re-run after n = 50000.

# At n = 50000, all gmos runs so far are seg faulting 

##################
### Conditions ###
##################

# Git: 74b9c7c5ff7d841dddbadaa6810684fa399b9d6b

# Calculate conditions
${NF}/src/2_conditions.sh

# UCHIME - no detections (all false or true negatives)
# F4_uchime.csv created manually in src/2_conditions.Rmd

# gmos - identical sequences are recombinant, not assessed further

#################
### Empirical ###
#################

# Git: bd30dda72e389bb422698a02c9d760acb68bbfbb

# Make maximum likelihood phylogenies
iqtree2 -s data/bcov.fasta -alrt 1000 -B 1000
iqtree2 -s data/bvdv.fasta -alrt 1000 -B 1000

# Git: 

# Detect recombination in empirical data
nextflow run ~/rec-bench/empirical.nf --out /shared/homes/13444841/2105_empirical

# Parse empirical outputs for plotting
ls /Users/13444841/Dropbox/Masters/02_working/2105_empirical/*.rec | xargs -I {} -n 1 python3 bin/parse_3seq_empirical.py {}
python3 bin/F3_concat_gc_outputs.py /Users/13444841/Dropbox/Masters/02_working/2105_empirical/
# F3_geneconv_summarised.csv manually formatted
python3 bin/F5_parse_gmos.py /Users/13444841/Dropbox/Masters/02_working/2105_empirical/
