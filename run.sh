#!/bin/bash

nextflow run main.nf --mode sim --seq data/FP7_patient_061_allseqs.fasta -profile docker
