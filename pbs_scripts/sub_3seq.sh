#!/bin/bash

#PBS -l ncpus=4
#PBS -l mem=64GB
#PBS -l walltime=72:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow 3seq_lean.nf -with-timeline 3seq_s_timeline.html -with-report 3seq_s_report.html
