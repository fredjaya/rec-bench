#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 18:04:18 2020

@author: 13444841
"""

import glob
import re
import pandas as pd
import csv
import argparse
from functools import reduce
from math import isnan
from numpy import unique

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
    return df.groupby(cols_stay) \
             .agg({'bp': my_lambda}) \
             .reset_index()

def read_sim_file():
    print("Reading simulated breakpoint file...")
    sim_path = "/Users/13444841/Dropbox/Masters/02_working/1911_precision_recall/191112_simbps/sim_bp_f1.csv"
    return pd.read_csv(sim_path)

def filter_seq_num(sim_bp):
    #https://stackoverflow.com/questions/28679930/how-to-drop-rows-from-pandas-data-frame-that-contains-a-particular-string-in-a-p/43399866
    sim_bp = sim_bp[~sim_bp['params'].str.contains("n2500")]
    sim_bp = sim_bp[~sim_bp['params'].str.contains("n5000")]
    return sim_bp

def match_breakpoints(bp):
    if type(bp) is str:
        s = set()
        for i in re.findall('\d+', bp):
            s.add(int(i))
        return s
    elif type(bp) is float: 
        return float('NaN')
    
def bp_to_set(sim_bp):
    d = []
    length = len(sim_bp)
    for index, sim_row in sim_bp.iterrows():
        print("{}/{}".format(index, length))
        d.append(match_breakpoints(sim_row['breakpoints']))
    return d
    
def amend_path(sim_bp):
    gc_path = "/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B3_geneconv/"
    sim_bp['params'] = sim_bp['params'].str.replace('fasta_Profile.csv', 'tab')
    sim_bp['params'] = gc_path + sim_bp['params'] 
    return sim_bp

def sim_in_gc(sim_row_param, gc_file):
    if gc_file.str.contains(sim_row_param).any():
        return True
    else:
        return False

def count_sim_bp(breakpoints):
    if type(breakpoints) == float:
        return 0
    else:
        return len(breakpoints)

def bp_length(bp):
    if type(bp) is set:
        return len(bp)
    elif type(bp) is float: 
        return 0
    
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
    grouped = group_params(gc)
    grouped.to_csv("F3_geneconv_out_groupedBP.csv")
    return grouped

def prep_sim_file():
    sim_bp = read_sim_file()
    sim_bp = filter_seq_num(sim_bp)
    sim_bp = amend_path(sim_bp)
    sim_bp['breakpoints'] = bp_to_set(sim_bp)
    return sim_bp
    
def count_conditions(sim_bp, gc):
    seq_length = 1680
    with open("F3_geneconv_conditions.csv", 'w+') as csv_file:
        writer = csv.writer(csv_file)
        csv_header = ['params', 'seq', 'TP', 'FP', 'TN', 'FN']
        writer.writerow(csv_header)
        
        for index, sim_row in sim_bp.iterrows():
            out_row = []
            out_row.append([sim_row['params']]) 
            out_row.append([sim_row['seq']])
            
            if sim_in_gc(sim_row.params, gc.file):
                
            else:
                TP = 0
                FP = 0
                TN = seq_length - bp_length(sim_row['breakpoints'])
                FN = bp_length(sim_row['breakpoints'])
                
                out_row.append(TP)
                out_row.append(FP)
                out_row.append(TN)
                out_row.append(FN)
                
                writer.writerow(out_row)

### Arguments -------------------- 
'''parser = argparse.ArgumentParser()
parser.add_argument("gc_dir", help = "path to dir containing geneconv output ()*.tab) files")
parser.add_argument("sim_bp", help = "simulated breakpoint file for each parameter and sequence")
args = parser.parse_args()
'''
### Main --------------------
gc = gc_to_dict()
sim_bp = prep_sim_file()

#conditions = count_conditions

