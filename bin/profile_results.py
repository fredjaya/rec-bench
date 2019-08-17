#!/bin/bash/python3

import glob
import csv
import re

fileNames = []

for f in glob.glob("out/S2_profile/*.csv"):
    fileNames.append(f)

with open('out/profile_s_stats.csv', 'w+') as csvfile:
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
        params = params[2:7]
        # get breakpoint p-values
        pval = open(n, 'r').read()
        pval = re.findall('(?<=\d, ).*(?=\n)', pval)
        writer.writerow(params + pval)
print("Writing to profile_s_stats.csv")
