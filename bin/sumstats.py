#!/usr/bin/env python3

import csv
import re
import glob

# Set regex patterns
regex_name = re.compile('[a-z]+')
regex_pval = re.compile(r'\d+\.\d+[e][+|-]\d+|(?<=\s)--(?=\n)')
# Need to account for '--' in tests other than Phi (Normal)
# Append log files to list
files = []
for file in glob.glob("out/S1_phipack/*.log"):
    files.append(file)

# Loop through output files to parse parameters and p-values
with open('sumstats.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['theta', 'rho', 'rep', 'NSS', 'MaxChi', 'PhiPerm', 'PhiNorm'])
    for file in files:
        phi = open(file, 'r').read()
        name = re.sub(regex_name, '', file)
        name = name.split("_")
        name = name[2:5]
        pvals = re.findall(regex_pval, phi)
        writer.writerow(name + pvals)
