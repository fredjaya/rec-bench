#!/usr/bin/env python3

"""
IN: santa-sim .fasta files
OUT:
"""
import csv
import re
import glob
import argparse

### Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument("sim_path", help = "path to dir containing santa-sim .fasta")
args = parser.parse_args()

### Functions ----------
def get_file_names(sim_path):
    file_names = []
    full_path = ("{}/*.fasta").format(sim_path)
    for f in glob.glob(full_path):
        file_names.append(f)
    return file_names

def parse_params(name):
    p = re.sub(r'^.*(?=msa)', '', name)
    p = re.sub(r'[a-z]+', '', p)
    p = p.split("_")
    return p[1:6]

def make_bp_csv(file_names):
    with open("V5_bp_stats.csv", 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        writer.writerow(['mut', 'rec', 'seqnum', 'dualInf', 'rep', 'seq', 'bps'])

        for f in file_names:
            params = parse_params(f)

            with open(f, 'r') as fasta:
              for line in fasta:
                  out_row = params.copy()
                  print(out_row)

                  if line.startswith('>'):
                      line = re.sub('>', '', line)
                      line = re.sub('\n', '', line)

                      if re.search(':', line):
                          line = line.split(':')
                          out_row = out_row + line
                          writer.writerow(out_row)

                  else:
                      out_row.append(line)

    return

### Main ----------
file_names = get_file_names(args.sim_path)
make_bp_csv(file_names)
