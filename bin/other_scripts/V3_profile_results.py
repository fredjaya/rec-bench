#!/bin/bash/python3

import glob
import csv
import re
import os
import sys

#setwd based on ${params.out}
path_in = sys.argv[1]
os.chdir(path_in)

fileNames = []

print("Reading PhiPack (Profile) outputs...")
for f in glob.glob("*.csv"):
    fileNames.append(f)

with open('B1_profile_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    # open a file to set the colnames/breakpoint bins
    f = open(fileNames[0], 'r').read()
    bp = re.findall('\d+(?=,)', f)
    head = ['mut', 'rec', 'seqLen', 'dualInf', 'rep']
    writer.writerow(head + bp)
    # get parameters
    for n in fileNames:
        params = re.sub('[a-z]+', '', n)
        params = params.split("_")
        params = params[1:6]
        # get breakpoint p-values
        pval = open(n, 'r').read()
        pval = re.findall('(?<=\d, ).*(?=\n)', pval)
        writer.writerow(params + pval)
print("Writing to B1_profile_stats.csv")
