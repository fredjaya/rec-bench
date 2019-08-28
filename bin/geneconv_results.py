#!/usr/bin/python3

import glob
import re
import csv

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

with open('/Users/13444841/GitHub/rec-bench/out/geneconv_s_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
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
print("Writing to out/geneconv_s_stats.csv")


# 6 inner fragments listed.
