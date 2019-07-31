#!/bin/bash

#PBS -l ncpus=2
#PBS -l mem=2GB
#PBS -l walltime=12:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow rdm-n2500.nf -with-timeline out/n2500_timeline.html -with-report out/n2500_report.html -with-trace out/n2500_trace.html
