#!/bin/bash

nextflow run main.nf --mode bm \
                     --seqn 100 \
                     --label pbs_small \
		                --out /shared/homes/13444841/out_190917 \
                      -profile conda \
		               --trace false
