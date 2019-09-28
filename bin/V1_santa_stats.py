#!/usr/bin/python3

import glob
import csv
import re
import os
import sys

#setwd
# TO DO: # Change to ${params.out}
path_in = sys.argv[1]
os.chdir(path_in)

# Append fasta files / filenames to list
fileNames = []

print("Reading santa stats files...")
for file in glob.glob("stats_*.csv"):
    fileNames.append(file)

with open('V1_santa_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    # write header
    writer.writerow([
        'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'generation',
        'population_size', 'mean_diversity', 'max_diversity',
        'min_fitness', 'mean_fitness', 'max_fitness', 'max_frequency',
        'mean_distance'
        ])
    for file in fileNames:
        # parse file name
        params = re.sub('stats_', '', file)
        params = re.sub('.csv', '', params)
        params = re.sub('out/santa/', '', params)
        params = re.sub('[a-z]', '', params)
        params = params.split('_')
        # parse row with santa stats
        f = open(file, 'r').read()
        f = f.split('\n')
        f = f[1].split(',')
        writer.writerow(params + f)
