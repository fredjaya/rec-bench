# rec-bench
Automated benchmarking of recombination detection methods

Eternally a WIP - many things are hardcoded

## Dependencies
Nextflow
conda

## Installation
```
git clone https://github.com/fredjaya/rec-bench.git
```

Nextflow doesn't appear to create the conda environment properly. Create manually.

```
conda env create -f environment.yml
conda activate fredjaya-rec-bench-0.1.0
```

Note: conda processes currently hardcoded in `main.nf`

## Usage
`rec-bench` has five modes that must be specified with `--mode` as follows:

`--mode sim`	Generate simulation datasets
`--mode sim_v`	Visualise/summarise simulation outputs
`--mode div`	Benchmark recombination detection methods using simulated data
`--mode emp`	Detect recombination in empirical sequence alignments
`--mode class`	Calculate classification metrics

`nextflow run main.nf --help`

- [ ] Update readme
