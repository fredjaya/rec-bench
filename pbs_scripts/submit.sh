#!/bin/bash

#PBS -l ncpus=4
#PBS -l mem=32GB
#PBS -l walltime=12:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd rec-bench
nextflow run hcv_minimal_hpc.nf --with-timeline timeline.html --with-report report.html
