#!/bin/bash

#PBS -l select=1:ncpus=1:mem=1GB
#PBS -l walltime=120:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow rdm-n2500_geneconv.nf -with-timeline out/n2500_geneconv_timeline.html -with-report out/n2500_geneconv_report.html -with-trace out/n2500_geneconv_trace.html
