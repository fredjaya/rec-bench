# rec-bench
automated benchmarking of recombination detection methods

```
nextflow run fredjaya/rec-bench --help
```

The typical command for running the pipeline is as follows:
```
nextflow run fredjaya/rec-bench --mode [sim/rdm/emp]
```

Mandatory arguments:
```
  --mode sim      Generate simulation datasets
  --mode bm       Detect recombination in simulated datasets and benchmark methods
  --mode emp      Detect recombination in empirical sequence alignments
  --mode viz      Parse simulation and analysis outputs for analysis
  --mode div      Divide sequence simulations by size for `--mode bm`
  --seq [.fasta]  Path to input .fasta file
```

Optional arguments:
```
  --seqn  [int]     Required for '--mode bm'. Sequence number for benchmark analysis
  --out   [str]     Name of output folder
  --xml   [.xml]    SANTA-SIM .xml configuration. Defaults to santa.xml
  --label ['str']   PBS queue label for '--mode bm' e.g. 'pbs_small' 'pbs_med'
  --trace [t/f]     Enables/disables tracing. Disable for testing and non `--mode bm`
```
