#!/usr/bin/env python3

from Bio import SeqIO
import re

f_out_m = open("data/fmdv/FMDV_Kenya_4refs_alg_m.fasta", "w")

with open("data/fmdv/FMDV_Kenya_4refs_alg.fasta", "r") as f_in:
    # Replace characters in header with '_' for downstream analyses
    for f_in in f_in:
        f_out_m.write(re.sub('([()\/])', '_', f_in))

f_out_n = open("data/fmdv/FMDV_Kenya_4refs_alg_n.fasta", "w")

with open("data/fmdv/FMDV_Kenya_4refs_alg_m.fasta") as f_out_m:
    # Delete gaps from sequences
    f_out_m = f_out_m.readlines()
    for line in f_out_m:
        if line.startswith('>'):
            f_out_n.write(line)
        if not line.startswith('>'):
            f_out_n.write(re.sub('-', '', line))
