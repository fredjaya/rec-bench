#!/bin/bash

nextflow run main.nf --mode emp \
		     --label pbs_med \
		     --seq FP7_patient_037_allseqs.fasta \
		     -profile conda
