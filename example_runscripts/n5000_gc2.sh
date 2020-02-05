#!/bin/bash

nextflow run main.nf --mode bm \
		     --seqn 5000 \
       	 	     --label pbs_small \
		     --out /shared/homes/13444841/200204_n5000_gc2 \
		     --simdir /shared/homes/13444841/200112_n5000_3seq_gc/gc2_in
