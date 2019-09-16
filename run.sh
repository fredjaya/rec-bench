#!/bin/bash

nextflow run main.nf --mode sim --seq data/FP7_patient_037_allseqs.fasta -profile conda
