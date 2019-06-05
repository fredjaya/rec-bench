#!/usr/bin/env python3

import sys
import re
from collections import Counter
from matplotlib import pyplot as plt

# Check argument
if len(sys.argv) < 2:
    print("Please specify a .fasta file!")
    exit()
if len(sys.argv) > 2:
    print("Too many arguments! Please specify one .fasta file.")
    exit()
if len(sys.argv) == 2:
    data = sys.argv[1]
    print("||\n"
          "||  Reading", data, "...")

# Define functions
def seqLenHist( seqLength, maxseq, minseq, x ):
    if (maxseq - minseq) <= 1:
        print("||  All sequences are", maxseq, "bp\n||")
    if (maxseq - minseq) > 1:
        print("||   Longest sequence is %i" % maxseq, "\n"
              "||  Shortest sequence is %i" % minseq, "\n"
              "||  Plotting sequence length frequencies to seqLengthFHist" + x + ".png...\n||")
        plt.hist(seqLength, bins = range(minseq, maxseq + 1, 1), align = 'right')
        plt.savefig("seqLengthFHist"+ x + ".png")

# Set string for I/O files
data_m = data + "_m" # [m]odified sequence names
data_n = data + "_n" # [n]o gaps in sequences

# Set list for sequence lengths
seqLengthA = []
seqLengthB = []

with open(data, "r") as f_in:
    # Replace characters in header with '_' for downstream analyses
    f_out_m = open(data_m, "w")
    for f_in in f_in:
        f_out_m.write(re.sub('([()\/])', '_', f_in))

with open(data_m) as f_out_m:
    # Delete gaps from sequences
    f_out_n = open(data_n, "w")
    f_out_m = f_out_m.readlines()
    for line in f_out_m:
        if line.startswith('>'):
            f_out_n.write(line)
        if not line.startswith('>'):
            seqLengthA.append(len(line))
            f_out_n.write(re.sub('-', '', line))

with open(data_n) as f_out_n:
    # Find the max sequence length of gapless alignment
    f_out_n = f_out_n.readlines()
    for line in f_out_n:
        if not line.startswith('>'):
            seqLengthB.append(len(line))

# Plot sequence length histogram of original input alignment
maxseqA = max(seqLengthA)-1
minseqA = min(seqLengthA)-1
seqLenHist(seqLengthA, maxseqA, minseqA, "A" )

# Plot histogram after gaps have been removed
print("||  Removing all gaps in", data, "...\n||")
maxseqB = max(seqLengthB)-1
minseqB = min(seqLengthB)-1
seqLenHist(seqLengthB, maxseqB, minseqB, "B" )

#print(maxseqB - max0seqB)
# Attempting to remove all files with -
"""
f_out_n2 = open("data/fmdv/FMDV_Kenya_4refs_alg_n2.fasta", "w")
re_max = r">.+\n\w{" + str(maxseq) + r"}\n"

with open("data/fmdv/FMDV_Kenya_4refs_alg_n.fasta", "r") as f_out_n:
    f_out_n = f_out_n.read()
    f_out_n2.write(re.findall(re_max, f_out_n))
"""
