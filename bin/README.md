# Binaries and scripts
### SANTA-SIM
`santa-ba8733a.jar`
* needs to be added into a `.sif`

`fasta_preprocess.py`
* filters and edits sequences for programs that cannot handle hyphens `-` i.e. santa-sim, UCHIME

`sim_bp.py` and `sim_bp.R`
* parse `.fasta` headers for breakpoints

`santa_stats.py` and `santa_stats.R`
* parses SANTA-SIM stats.csvs and plots stats (PCA etc.)

### PhiPack
`phi_results.sh` runs the following scripts:
* `phi_results.py` parses phi simulation results for viz
* `phi_results.R` generates viz

### Profile
`profile_results.py` and `profile_results.R`
* parses Profile outputs and plots

### 3SEQ
Need `3seq_results.py` to parse breakpoints for all runs i.e. start/end hists

`3seq_results.R`
* Plots 3SEQ breakpoint locations for each sequence, one replicate only

### GENECONV
`geneconv_results.py` and `geneconv_results.R`
* plots facets of start/end breakpoints

### Nextflow trace
`trace.py` and `trace.R`
* parses Nextflows trace output, converting everything to hours, and plots times per method
