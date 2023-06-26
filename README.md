# rec-bench
Automated benchmarking of recombination detection methods

(Note: many things are hardcoded)  

## Dependencies  
Nextflow 22.10 (DSL1-compatible)  
conda  

## Installation  
```
# Download repo
git clone https://github.com/fredjaya/rec-bench.git

# Generate p-value table for 3SEQ
bin/3seq_elf -gen-p bin/p700 700
```

Install openrdp according to 
If Nextflow doesn't appear to create the conda environment properly. Create manually.

```
conda env create -f environment.yml
conda activate fredjaya-rec-bench-0.1.0
```

## Usage  

### Scalability  

```
nextflow run sim.nf \
	--mode scalability \
	--seq data/FP7_patient_037_allseqs.fasta \
	--xml data/neutral.xml \
	--out `pwd` 
```
