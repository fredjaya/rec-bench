#!/bin/bash

nextflow run main.nf --mode bm \
		     --out ./out_190917 \
		     --seqn 1000 \
		     --label 'pbs_small' \
		      -profile conda
