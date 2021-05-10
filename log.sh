## Generate new simulated dataset where:
# 1. 99 generations of mutation only (m = 0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3)
# 2. 1 generation of recombination only (r = 0, 0.001, 0.005, 0.01, 0.05, 0.1; d = 0, 1)

# On UTS HPCC
mkdir -p /shared/homes/13444841/2104_pub
export OUT=/shared/homes/13444841/2104_pub
export NF=/shared/homes/13444841/rec-bench
cd $OUT

nextflow run ${NF}/sim.nf \
	--seq ${NF}/data/FP7_patient_037_allseqs.fasta \
	--xml ${NF}/data/neutral.xml \
	--out ${OUT}

