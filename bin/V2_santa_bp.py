#!/usr/bin/env python3

"""
 IN: All simulated .fasta files
OUT: .csv of per sequence simulation parameters and brekpoint locations 
"""

import csv
import re
import glob
import os
import argparse

# Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument("sim_path",
    help = "path to dir containing simulation outputs '/S4_santa'")
args = parser.parse_args()

# Functions ----------
def set_path(sim_path):
    return os.path.join(sim_path, "**/*.fasta")

def get_file_names(joined_path):
    file_names = []
    print("Reading santa stats files ...")
    for file in glob.glob(joined_path):
        file_names.append(file)
    return file_names

def parse_names(fasta):
    p = re.sub('^.*(?=msa)', '', fasta) 
    p = re.sub('[a-z]', '', p)
    p = p.split('_')
    return p[1:6]

def check_bp(seq_bp):
    if re.findall(':', seq_bp):
        return seq_bp.split(':', 1)
    else:
        return [seq_bp] # so it matches the if case

def parse_fasta_header(fasta_line):
    seq_bp = re.sub('>', '', fasta_line)
    seq_bp = re.sub('\n', '', seq_bp)
    seq_bp = check_bp(seq_bp)
    return seq_bp

def parse_fasta_lines(fasta, params, writer):
    with open(fasta, 'r') as f:
        for line in f:
            if line.startswith('>'):
                out_row = params.copy()
                line = parse_fasta_header(line)
                out_row.extend(line)
                writer.writerow(out_row)
    return

def concat_fasta_headers(file_names):
    with open('V2_santa_bp.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        header = (['mut', 'rec', 'seqnum', 'dualInf', 'rep', 'seq', 'bps'])
        writer.writerow(header)
            
        for fasta in file_names:
            params = parse_names(fasta)
            parse_fasta_lines(fasta, params, writer)

# Main ----------
joined_path = set_path(args.sim_path)
file_names = get_file_names(joined_path)
concat_fasta_headers(file_names)
 
