#!/usr/bin/env python3

import csv
import re

# Set regex patterns
regex_name = re.compile('[a-z]+')
regex_pval = re.compile('\d+\.\d+[e][+|-]\d+')

# Input text
name = "msa_m0.0010_rc0.0000010_rep1_.fasta_Phi.log"
pvals = """NSS:                 1.00e+00  (1000 permutations)
Max Chi^2:           1.19e-01  (1000 permutations)
PHI (Permutation):   8.26e-01  (1000 permutations)
PHI (Normal):        3.27e-01
"""

# Split input file name
name = re.sub(regex_name, '', name)
name = name.split("_")
name = name[1:4]

# Match pvalues
pvals = re.findall(regex_pval, pvals)

with open('/out/sumstats.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['theta', 'rho', 'rep', 'NSS', 'MaxChi', 'PhiPerm', 'PhiNorm'])
    writer.writerow(name + pvals)
    # add seqlength
