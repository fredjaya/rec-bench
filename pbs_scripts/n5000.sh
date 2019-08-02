#!/bin/bash

#PBS -l ncpus=2
#PBS -l mem=2GB
#PBS -l walltime=168:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow rdm-n5000.nf -with-timeline out/n5000_timeline.html -with-report out/n5000_report.html -with-trace out/n5000_trace.html
