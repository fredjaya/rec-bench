"""
Summarise all geneconv outputs (*.tab) into one file to use as input for calculating
classification metrics
"""

import argparse
import glob
import re
import csv

# Functions ----------
def get_file_names(gc_dir):
    file_names = []
    for name in glob.glob("{}/*.tab".format(gc_dir)):
        file_names.append(name)
    return file_names

def parse_params(name):
    """ Split file name into individual parameters """
    print(name)
    p = re.sub('^.*(?=msa)', '', name)
    p = re.sub('[a-z]+', '', p) 
    p = p.split("_")
    return p[1:6]

def gc_colnames():
    column_names = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', \
                    'frag_type', 'seq_names', 'sim_pval', 'BC_KA_pval', \
                    'aligned_start', 'aligned_end', 'aligned_length', \
                    'seq1_begin','seq1_end', 'seq1_length', 'seq2_begin', \
                    'seq2_end', 'seq2_length', 'num_poly', 'num_dif', \
                    'total_diffs', 'mismatch_penalty']
    return column_names

def prep_row(name, line):
    params = parse_params(name)
    print(params)
    scores = line.split('\t')
    scores = scores[0:17]
    params.insert(0, name)
    row = params + scores
    return row

def gc_to_csv(file_names):
    with open("F3_geneconv_summarised.csv", "w+") as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        writer.writerow(gc_colnames())

        for f in file_names:
            print(f)
            with open(f, 'r') as gc:
                for line in gc:
                    if re.findall('^GI', line):
                        row = prep_row(f, line)
                        print("[GI]", row)
                        writer.writerow(row)

                    if re.findall('^GO', line):
                        row = prep_row(f, line)
                        print("[GO]", row)
                        writer.writerow(row)
    return

# Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument("gc_dir", help = "path to geneconv output files (*.tab) e.g. project/B3_geneconv")
args = parser.parse_args()

# Main ----------
file_names = get_file_names(args.gc_dir)
print(file_names)
gc_to_csv(file_names)
