#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 08:01:14 2020

@author: Fred Jaya
"""

import glob
import re
import pandas as pd
import csv
import argparse
from functools import reduce

### Functions --------------------
def gc_file_names(gc_dir):
    print("Reading in *.tab files from {}".format(gc_dir))
    gc_file_names = []
    for name in glob.glob("{}*.tab".format(gc_dir)):
        gc_file_names.append(name)
    return(gc_file_names)

def parse_params(name):
    """ Split file name into individual parameters """
    r_dir = re.compile(rf'(?<={args.gc_dir}).*')
    r_alphas = re.compile(r'[a-z]+')

    p = re.findall(r_dir, name)
    p = re.sub(r_alphas, '', p[0])
    p = p.split("_")
    p = p[1:6]
    return(p)

def gc_colnames():
    column_names = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', \
                    'frag_type', 'seq_names', 'sim_pval', 'BC_KA_pval', \
                    'aligned_start', 'aligned_end', 'aligned_length', \
                    'seq1_begin','seq1_end', 'seq1_length', 'seq2_begin', \
                    'seq2_end', 'seq2_length', 'num_poly', 'num_dif', \
                    'total_diffs', 'mismatch_penalty']
    return(column_names)
   
def gc_prep_row(name, line):
    params = parse_params(name)
    scores = line.split('\t')
    scores = scores[0:17]
    params.insert(0, name)
    row = params + scores
    return(row)

def gc_to_csv(file_names):
    with open("F3_geneconv_out.csv", "w+") as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        writer.writerow(gc_colnames())
        for name in file_names:
            with open(name, 'r') as gc_file:
            # https://stackoverflow.com/a/34240726/7681828
                print(name)
                for line in gc_file:
                    # TODO: refactor to function?
                    if re.findall('^GI', line):
                        row = gc_prep_row(name, line)
                        writer.writerow(row) 

def read_gc_file(file_name):
    return pd.read_csv(file_name)

def rm_cols(df):
    return df.drop(columns =
                 ['sim_pval', 'BC_KA_pval', 'aligned_start', 'aligned_end', \
                  'aligned_length', 'num_poly', 'total_diffs', 'bp_length'])

def bp_pairs_to_set(df):
    bp = []
    df = df[['start_bp', 'end_bp']]
    for index, row in df.iterrows():
        bp.append({row['start_bp'], row['end_bp']})
        print(len(bp))
    return bp

def append_bps(df, bp):
    return df.assign(bp = bp)

def rm_bp_pairs(df):
    return df.drop(columns = ['start_bp', 'end_bp'])

def unite_bp(df):
    return set.union(*df['bp'].tolist())

def group_params(df):
    #https://stackoverflow.com/questions/25020595/row-wise-unions-in-pandas-groupby
    cols_stay = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', 'seq_name']
    my_lambda = lambda x: reduce(set.union, x) 
    grouped = df.groupby(cols_stay)
    return grouped.agg({'bp': my_lambda})

def read_sim_file(sim_bp):
    return(open(sim_bp, 'r'))

### Big functions
def concat_gc_outputs():
    file_names = gc_file_names(args.gc_dir)
    gc_to_csv(file_names)

def gc_to_dict(): 
    gc = read_gc_file("/Users/13444841/Dropbox/Masters/02_working/2002_geneconv_conditions/F3_geneconv_out_mergedSeq.csv")
    gc = rm_cols(gc)
    bp = bp_pairs_to_set(gc)
    gc = append_bps(gc, bp)
    gc = rm_bp_pairs(gc)
    gc = group_params(gc)
    gc.to_csv("F3_geneconv_out_groupedBP.csv")  
    return gc
    
### Arguments -------------------- 
'''parser = argparse.ArgumentParser()
parser.add_argument("gc_dir", help = "path to dir containing geneconv output ()*.tab) files")
parser.add_argument("sim_bp", help = "simulated breakpoint file for each parameter and sequence")
args = parser.parse_args()
'''
### Main --------------------

