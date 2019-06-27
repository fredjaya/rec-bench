#!/usr/bin/env python3

import csv
import re
import glob

# Set regex patterns
regex_pval = re.compile(r'\d+\.\d+[e][+|-]\d+|(?<=\s)--(?=\n)')
# Need to account for '--' in tests other than Phi (Normal)

# Append log files to list
simLogs = []
print(" Reading Phi .log files...")
for logFile in glob.glob("out/S1_phipack/*.log"):
    simLogs.append(logFile)

# Loop through output files to parse parameters and p-values
with open('out/phipack_s_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['theta', 'rho', 'seqLen', 'rep', 'NSS', 'MaxChi', 'PhiPerm', 'PhiNorm'])
    for logFile in simLogs:
        phi = open(logFile, 'r').read()
        name = re.sub('[a-z]+', '', logFile)
        name = name.split("_")
        name = name[2:6]
        pvals = re.findall(regex_pval, phi)
        writer.writerow(name + pvals)

print(" Writing to 'out/phipack_s_stats.csv'.")
