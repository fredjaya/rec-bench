#!/usr/bin/env python3

import csv
import re
import glob
import os

#setwd
# Change to ${params.out}
path = "/Users/13444841/GitHub/rec-bench/out/S4_santa"
os.chdir(path)

# Append fasta files / filenames to list
fileNames = []

print("Reading santa stats files...")
for file in glob.glob("msa_*.fasta"):
    fileNames.append(file)
    print(file)

with open('V1_bp_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['mut', 'rec', 'seqL', 'dualInf', 'rep', 'bps'])

    for name in fileNames:
        # Parse file names for parameters
        params = re.sub('[a-z]+', '', name)
        params = params.split("_")
        params = params[1:]
        print(name)
        print(params)
        with open(name) as file:
            for line in file:
                paramsNew = params.copy()
                if line.startswith('>'):
                    if re.search(':', line):
                        line = line.split(':')
                        paramsNew.append(line)
                        #print("YES BP: " +str(paramsNew))
                        writer.writerow(paramsNew)
                    else:
                        paramsNew.append(line)
                        #print("no bps: " + str(paramsNew))
                        writer.writerow(paramsNew)
