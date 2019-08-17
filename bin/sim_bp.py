#!/usr/bin/env python3

import csv
import re
import glob
import os

# Append fasta files / filenames to list
fileNames = []

print("Reading simulated .fasta files...")
for file in glob.glob("out/simfasta/*.fasta"):
    # simfasta is a folder with all fasta files, likely deleting this in future
    # versions as it's a dupe of santa/n* folders
    fileNames.append(file)

bp_counter = 0
no_bp_counter = 0

with open('out/sim_bp_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['mut', 'rec', 'seqL', 'dualInf', 'rep', 'bps'])

    for name in fileNames:
        # Parse file names for parameters
        params = re.sub('[a-z]+', '', name)
        params = params.split("_")
        params = params[1:]
        with open(name) as file:
            for line in file:
                paramsNew = params.copy()
                if line.startswith('>'):
                    if re.search(':', line):
                        line = line.split(':')
                        paramsNew.append(line)
                        bp_counter += 1
                        writer.writerow(paramsNew)
                    else:
                        paramsNew.append(line)
                        writer.writerow(paramsNew)
                        no_bp_counter += 1
print('Sequences with breakpoints: ' + str(bp_counter) + '\n' + \
 'Sequences without breakpoints ' + str(no_bp_counter))
