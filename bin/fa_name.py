#!/usr/bin/env python3

import re

re_fasta_name = re.compile('([()\/])')

f_out = open('data/fmdv/FMDV_Kenya_4refs_alg_m.fasta', 'w')
f_in = open('data/fmdv/FMDV_Kenya_4refs_alg.fasta')

for line in f_in:
    f_out.write(re.sub(re_fasta_name, '_', line)
