# rec-bench
automated benchmarking of recombination detection methods

[![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/3131)

# Dependencies
* Singularity 2.6.1
* Nextflow 19.04.1 (to be added to .simg)

# Nextflow scripts
#### hcv_minimal_hpc.nf
* Runs on the HPC using Singularity containers
* Currently runs Phi with full empirical and simulated data

#### empirical.nf
* OSX only
* Runs RDMs only on empirical datasets

#### other .nf files
* Runs on OSX with local binaries
* For initial testing and proof of concept
