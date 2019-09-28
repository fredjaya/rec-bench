# rec-bench
automated benchmarking of recombination detection methods

Update readme.

## To-do
- [ ] add/fix process to visualise simulation outputs
- [x] test PhiPack with conda
- [ ] add 3seq or geneconv to conda
- [ ] split conda recipes based on `--mode`

**S1_filter_fasta**
- [ ] Needs a better way to deal with sequence gaps
- [ ] Output final sequence length?

**S2_santa_xml**
- [ ] read in sequence length from S1

**S3_param_sweep**
- [ ] make parameter config file

**S4_santa**
- [ ] add `santa_bp.jar` in conda/docker/sing

**V1_santa_stats**
- [x] fix python script
- [ ] implement R script

**sim_v general**
- [ ] amend inputs
**B1_phi_profile**
- [ ]

### Low priority
- [ ] ? Change --mode x/y/z to --x/--y/--z
- [ ] Add path to santa.jar in docker image

**Config**
- [ ] add profiles for local, HPC
- [ ] specify queue based on seqnum
- [ ] look into setting `executor{queueSize = n}` based on queue
