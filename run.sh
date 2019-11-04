#!/bin/bash

nextflow run main.nf --mode viz \
		     --out /Users/13444841/Dropbox/Masters/03_results/out_190929 \ 
		      -profile conda \
		     --trace false
