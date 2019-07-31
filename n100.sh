#!/bin/bash

#PBS -l ncpus=2
#PBS -l mem=2GB
#PBS -l walltime=12:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow rdm-n100.nf -with-timeline n100_timeline.html -with-report n100_report.html -with-trace n100_trace.html
