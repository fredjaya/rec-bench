#!/bin/bash

nextflow run /shared/homes/13444841/rec-bench/main.nf \
	--mode sim \
	--seq /shared/homes/13444841/rec-bench/data/FP7_patient_037_allseqs.fasta \
	--out /shared/homes/13444841/2002_full_analysis/sim \
	-profile conda

