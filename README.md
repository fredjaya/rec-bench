# rec-bench
automated benchmarking of recombination detection methods

[![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3131)

# Dependencies
* Singularity 2.6.1
* Nextflow 19.04.1 (to be added to .simg)

# Folders and files
* `hcv_minimal_hpc.nf` most up-to-date and functional nextflow script. Runs PhiPack only.
* `hcv_santa.xml` evolutionary parameters for HCV
* `nextflow.config` specifies Singularity images for pipeline processes
* `clean.sh` removes nextflow outputs (logs, work dir, output files)


### bin
* Recombination detection binaries
* Simulation binary
* Output visualisation and pre-processing scripts

### data
Sequence files for testing/proof of concept and analyses

### nf_scripts
Old nextflow scripts - outdated/needs updating

Mainly for use on local OSX machine

### pbs_scripts
Submission scripts for HPC jobs

### simg
Singularity images for build on shub
