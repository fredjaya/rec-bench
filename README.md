# rec-bench
Automated benchmarking of recombination detection methods

Eternally a WIP - many things are hardcoded

## Dependencies  
Nextflow  
conda  

## Installation  
```
# Download repo
git clone https://github.com/fredjaya/rec-bench.git

# Generate p-value table for 3SEQ
bin/3seq_elf -gen-p bin/p700 700
```

If Nextflow doesn't appear to create the conda environment properly. Create manually.

```
conda env create -f environment.yml
conda activate fredjaya-rec-bench-0.1.0
```

## To-do
- [ ] Add to bioconda:  
	- [ ] 3SEQ  
	- [ ] GENECONV  
	- [ ] SANTA-SIM  
- [ ] Create docker/singularity containers
- [ ] Update readme
