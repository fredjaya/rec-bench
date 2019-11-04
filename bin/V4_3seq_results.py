#!/usr/bin/python3

import glob
import re
import csv
import pandas as pd
import os
import sys

# functions
def parse_params(name):
    # Get parameters from file names and tabulate
    p = re.sub('\.fasta\.3s\.rec', '', name)
    p = re.sub('[a-z]+', '', p)
    p = p.split("_")
    p = p[1:6]
    return(p)

path_in = sys.argv[1]
os.chdir(path_in)

print("Writing to B2_3seq_stats.csv...")
fileNames = []

for f in glob.glob("*.3s.rec"):
    fileNames.append(f)

with open('B2_3seq_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    head = ['mut', 'rec', 'seqLen', 'dualInf', 'rep', 'P_ACCNUM', 'Q_ACCNUM', \
            'C_ACCNUM', 'm', 'n', 'k', 'p', 'HS?', 'log(p)', 'DS(p)', \
            'DS(p)2', 'min_rec_length', 'breakpoints']
    writer.writerow(head)
    for name in fileNames:
        with open(name, 'r') as file:
            params = parse_params(name)
            line_count = 0
            na_row = ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', \
                      'NA', 'NA', 'NA', 'NA', 'NA']
            for line in file:
                # If no recombination was detected, output row of NAs
                line_count += 1
                if line_count == 1:
                    writer.writerow(params + na_row)
                else:
                    l = re.sub('\s&', '', line)
                    l = l.split()
                    writer.writerow(params + l)
