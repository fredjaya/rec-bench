#!/bin/bash

#PBS -l ncpus=4
#PBS -l mem=64GB
#PBS -l walltime=24:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

OMP_NUM_THREADS=4
export OMP_NUM_THREADS

cd rec-bench
nextflow run hcv_minimal_hpc.nf --with-timeline timeline.html --with-report report.html
