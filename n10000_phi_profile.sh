#!/bin/bash

#PBS -l select=1:ncpus=2:mem=2GB
#PBS -l walltime=168:00:00

#PBS -m abe
#PBS -M frederick.r.jaya@student.uts.edu.au

cd ~/rec-bench
nextflow rdm-n10000_phi_profile.nf -with-timeline out/n1000_phi_profile_timeline.html -with-report out/n10000_phi_profile_report.html -with-trace out/n10000_phi_profile_trace.html

