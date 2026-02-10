# rec-bench
Automated benchmarking of recombination detection methods using simulated and empirical datasets.

Associated publication: https://academic.oup.com/ve/article/9/2/vead066/7444193

## Repo Map
- `sim.nf`: Nextflow (DSL1) pipeline to simulate datasets with SANTA-SIM and benchmark multiple recombination detection methods (RDMs).
- `empirical.nf`: Nextflow pipeline to run RDMs on empirical FASTA datasets.
- `processes.nf`: Shared Nextflow processes for OpenRDP methods (`rdp`, `maxchi`, `chimaera`).
- `nextflow.config`: Default parameters, executors, and reporting/tracing configuration.
- `bin/`: Binaries and helper scripts for simulation parsing, conditions, and plotting inputs.
- `src/`: Rmd analysis notebooks, rendered HTML reports, and helper shell scripts for post-processing.
- `data/`: Input FASTA and SANTA-SIM XML templates plus parameter-sweep XMLs.
- `figs/`: Generated figures from the analysis notebooks.
- `tests/`: Python tests validating parsing and condition-calculation utilities.
- `log.sh`: A runnable “lab notebook” that documents the steps used for simulation, analysis, and empirical runs.

## Dependencies
- Nextflow 22.10 (DSL1-compatible)
- Conda environment defined in `environment.yml`

External tools used by the pipelines:
- SANTA-SIM (custom `bin/santa_bp.jar` included)
- PhiPack (`Profile`)
- 3SEQ (`bin/3seq_elf` included)
- GENECONV (`bin/geneconv` included)
- UCHIME via `vsearch`
- GMOS (`bin/gmos` included)
- OpenRDP (external; not included)

## Setup
Install the conda environment if Nextflow does not create it automatically:
```bash
conda env create -f environment.yml
conda activate fredjaya-rec-bench-0.1.0
```

Generate the 3SEQ p-value table once:
```bash
bin/3seq_elf -gen-p bin/p700 700
```

## Pipelines

### `sim.nf` — Simulation + Benchmarking
Simulates FASTA datasets over parameter sweeps and runs multiple RDMs.

Key inputs:
- `--mode`: `performance` or `scalability`
- `--seq`: input FASTA for SANTA-SIM seeding
- `--xml`: SANTA-SIM XML template
- `--out`: output directory

Example:
```bash
nextflow run sim.nf \
  --mode scalability \
  --seq data/FP7_patient_037_allseqs.fasta \
  --xml data/neutral.xml \
  --out "$(pwd)"
```

High-level steps in `sim.nf`:
- `S1_*` filter FASTA and prepare SANTA-SIM inputs
- `S3_*` parameter sweep of XMLs
- `S4_*` run SANTA-SIM
- `B*` run RDMs: PhiPack Profile, 3SEQ, GENECONV, UCHIME, GMOS
- `rdp/maxchi/chimaera` (OpenRDP) are included at the end of the file

### `empirical.nf` — Empirical Datasets
Runs RDMs on empirical datasets, producing raw tool outputs for downstream parsing and visualization.

Notes:
- Uses hardcoded input path glob and output directory inside `empirical.nf`. Update these before running on a new system.

### `processes.nf` — OpenRDP Methods
Contains reusable Nextflow processes for `rdp`, `maxchi`, and `chimaera` on an input FASTA channel (`params.fa`).

## Post-processing and Analysis
- `src/1_sim_stats.sh`: generates simulation stats and derived CSVs
- `src/2_conditions.sh`: computes TP/FP/TN/FN conditions for tools
- `src/*.Rmd`: analysis notebooks for performance, scaling, and empirical results
- `src/*.html`: rendered notebooks

The `log.sh` file documents a full run from simulation through plots, including manual steps and troubleshooting notes.

## `bin/` Scripts and Binaries
Key helpers include:
- `S1_filter_fasta.py`: removes gappy sequences for SANTA-SIM
- `V1_santa_stats.py`, `V2_santa_bp.py`, `V3_sim_bp.R`: derive true breakpoints and stats
- `F1_addCondition_phiProfile.py`, `F2_addCondition_3SEQ.py`, `F3_addCondition_geneconv2.py`: compute detection conditions
- `F3_concat_gc_outputs.py`, `F3_separate_seq_pairs.R`: GENECONV parsing
- `V4_sim_distances.R`, `V5_fasta_to_bpcounts.py`: additional simulation metrics
- Binaries: `3seq_elf`, `geneconv`, `gmos`, `santa_bp.jar`

## Tests
`tests/` contains tests for parsing and condition-calculation utilities (e.g., 3SEQ and PhiPack helpers, trace parsing).

## Caveats
- Many paths are hardcoded and may need to be tweaked for future runs
- Configuration is not optimised for efficiency
- Start with `log.sh` to see the exact commands and order used in the original runs.
- Use the provided `data/` inputs and `data/xml/` parameter-sweep templates to match published settings.
- Verify tool versions in `environment.yml` and in any external installations (OpenRDP, IQ-TREE, etc.).
