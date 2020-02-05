#!/bin/bash

nextflow run main.nf --mode bm \
		     --seqn 5000 \
       	 	     --label pbs_med \
		     --out /shared/homes/13444841/200112_n5000_3seq_gc \
		     --simdir /shared/homes/13444841/2001_gmos_sim2 \
		     -resume
