#!/bin/bash

#PBS -l select=1:cpus=1:mem=1GB
#PBS -l walltime=12:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow rdm-n1000.nf -with-timeline out/n1000_timeline.html -with-report out/n1000_report.html -with-trace out/n1000_trace.html
