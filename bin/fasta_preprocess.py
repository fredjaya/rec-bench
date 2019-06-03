#!/usr/bin/env python3

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

seqLength = []
with open("data/fmdv/FMDV_Kenya_4refs_alg_n.fasta") as f_out_n:
    # Find the max sequence length
    f_out_n = f_out_n.readlines()
    for line in f_out_n:
        if not line.startswith('>'):
            seqLength.append(len(line))
maxseq = max(seqLength)-1
print("\n", "Longest sequence is %i" % maxseq, "\n")
    # Manual inspection of sequence shows max is max-1???

# Attempting to remove all files with 
"""
f_out_n2 = open("data/fmdv/FMDV_Kenya_4refs_alg_n2.fasta", "w")
re_max = r">.+\n\w{" + str(maxseq) + r"}\n"

with open("data/fmdv/FMDV_Kenya_4refs_alg_n.fasta", "r") as f_out_n:
    f_out_n = f_out_n.read()
    f_out_n2.write(re.findall(re_max, f_out_n))
"""
