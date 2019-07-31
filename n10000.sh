#!/bin/bash

#PBS -l ncpus=2
#PBS -l mem=2GB
#PBS -l walltime=100:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow rdm-n10000.nf -with-timeline out/n10000_timeline.html -with-report out/n10000_report.html -with-trace out/n10000_trace.html

