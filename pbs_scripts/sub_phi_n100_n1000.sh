#!/bin/bash

#PBS -l ncpus=4
#PBS -l mem=64GB
#PBS -l walltime=72:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow run phi_n100_n1000.nf -with-timeline phi_timeline.html -with-report phi_report.html
