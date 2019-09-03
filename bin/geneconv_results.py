#!/usr/bin/python3

import glob
import re
import csv
import pandas as pd

# functions
def parse_params(name):
    # Get parameters from file names and tabulate
    p = re.sub('[a-z]+', '', name)
    p = p.split("_")
    p = p[2:7]
    return(p)

def inner(file):
    in_frags = re.findall('(?<=# )(No|One|\d+)(?= inner fragment)', file)
    return(in_frags)

def outer(file):
    out_frags = re.findall('(?<=# )(No|One|\d+)(?= outer-sequence fragment)', file)
    return(out_frags)

# script
fileNames = []
for f in glob.glob("/Users/13444841/GitHub/rec-bench/out/S4_geneconv/*.tab"):
    fileNames.append(f)

with open('/Users/13444841/GitHub/rec-bench/out/geneconv_s_stats_short.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    # Write csv with number of recombinaton 
    head = ['mut', 'rec', 'seqLen', 'dualInf', 'rep', 'inner', 'outer']
    writer.writerow(head)
    for n in fileNames:
        # get parameters
        params = parse_params(n)
        # check for inner/outer fragments detected
        file = open(n, 'r').read()
        i_frags = inner(file)
        o_frags = outer(file)
        writer.writerow(params + i_frags + o_frags)
print("Writing to out/geneconv_s_stats_short.csv")

with open('/Users/13444841/GitHub/rec-bench/out/geneconv_s_stats_long.csv', 'w+') as csvfile:
    print("Writing to out/geneconv_s_stats_long.csv")
    writer = csv.writer(csvfile, delimiter = ',')
    # Write colnames
    head = ['mut', 'rec', 'seqLen', 'dualInf', 'rep', \
            'frag_type', 'seq_names', 'sim_pval', 'BC_KA_pval', \
            'aligned_start', 'aligned_end', 'aligned_length', 'seq1_begin', \
            'seq1_end', 'seq1_length', 'seq2_begin', 'seq2_end', \
            'seq2_length', 'num_poly', 'num_dif', 'total_diffs', 'mismatch_penalty']
    writer.writerow(head)
    for n in fileNames:
        with open(n, 'r') as file:
            params = parse_params(n)
            for line in file:
                if re.findall('^GI', line):
                    l = line.split('\t')
                    #print(l)
                    writer.writerow(params + l)