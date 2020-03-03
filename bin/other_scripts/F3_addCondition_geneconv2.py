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
#import argparse
from functools import reduce
from math import isnan

### Functions --------------------
def gc_file_names(gc_dir):
    print("Reading in *.tab files from {}".format(gc_dir))
    gc_file_names = []
    for name in glob.glob("{}*.tab".format(gc_dir)):
        gc_file_names.append(name)
    return(gc_file_names) 

def params_resub(subject):
    r_alphas = re.compile(r'[a-z]+')
    
    p = re.sub(r_alphas, '', subject)
    p = p.split("_")
    p = p[1:6]
    return p

def parse_params_gc(name):
    """ Split file name into individual parameters """
    r_dir = re.compile(rf'(?<={args.gc_dir}).*')
    query = re.findall(r_dir, name)
    
    params_resub(query[0], r_alphas)
        
    p = re.sub(r_alphas, '', p[0])
    p = p.split("_")
    p = p[1:6]
    return p

def gc_colnames():
    column_names = ['file', 'mut', 'rec', 'seqLen', 'dualInf', 'rep', \
                    'frag_type', 'seq_names', 'sim_pval', 'BC_KA_pval', \
                    'aligned_start', 'aligned_end', 'aligned_length', \
                    'seq1_begin','seq1_end', 'seq1_length', 'seq2_begin', \
                    'seq2_end', 'seq2_length', 'num_poly', 'num_dif', \
                    'total_diffs', 'mismatch_penalty']
    return(column_names)
   
def gc_prep_row(name, line):
    params = parse_params_gc(name)
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

def match_files_seq(sim_row, gc):
    """ Check if sim params and seq is present as GC file and seq_name """
    #https://stackoverflow.com/questions/57208954/select-rows-that-match-values-in-multiple-columns-in-pandas
    sim_vals = [sim_row['params'], sim_row['seq']]
    gc_row = gc[(gc[['file', 'seq_name']] == sim_vals).all(1)]
    return gc_row

def bp_series_to_set(sim_row, gc):
    gc_row = match_files_seq(sim_row, gc)
    gc_bp = gc_row.iloc[0]['bp']
    return gc_bp
    
def sim_seq_in_gc(sim_row, gc):
    if match_files_seq(sim_row, gc).empty:
        return False
    else:
        return True

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

def true_pos(bp_sim, bp_gc):
    i = bp_sim.intersection(bp_gc)
    return len(i)

def false_pos(bp_sim, bp_gc):
    d = bp_gc.difference(bp_sim)
    return len(d)

def false_neg(bp_sim, bp_gc):
    d = bp_sim.difference(bp_gc) 
    return len(d)

def true_neg(seq_length, TP, FP, FN):
    return seq_length - TP - FP - FN

def append_out_row(TP, FP, TN, FN, out_row):
    out_row.append(TP)            
    out_row.append(FP)
    out_row.append(TN)
    out_row.append(FN)
    return out_row

def calc_no_gc(sim_row, seq_length, out_row):
    TP = 0
    FP = 0
    TN = seq_length - bp_length(sim_row['breakpoints'])
    FN = bp_length(sim_row['breakpoints'])
    return append_out_row(TP, FP, TN, FN, out_row)

def calc_yes_gc_no_sim(bp_gc, seq_length, out_row):
    TP = 0
    FP = bp_length(bp_gc)
    TN = seq_length - bp_length(bp_gc)
    FN = 0
    return append_out_row(TP, FP, TN, FN, out_row)

def calc_yes_gc_yes_sim(sim_row, gc, seq_length, out_row):
    TP = true_pos(sim_row['breakpoints'], gc)
    FP = false_pos(sim_row['breakpoints'], gc)
    FN = false_neg(sim_row['breakpoints'], gc)
    TN = true_neg(seq_length, TP, FP, FN)
    return append_out_row(TP, FP, TN, FN, out_row)

def parse_params_out(subject):
    r_path = re.compile(r'^/Users\/13444841\/Dropbox\/Masters\/03_results\/out_190925\/out_190917\/B3_geneconv')
    p = re.sub(r_path, '', subject)
    return params_resub(p)

def rcseq_no_gc(sim_bp):
    if type(sim_bp) is float:
        return 'TN'
    elif type(sim_bp) is set:
        return 'FN'

def getTPR(TP, FN):
    if (TP == 0 and FN == 0):
        return(float('NaN'))
    else:
        return(int(TP/(TP + FN)))

def getFPR(FP, TN):
    if (FP == 0 and TN == 0):
        return(float('NaN'))
    else:
        return(int(FP/(FP + TN)))

def getTNR(TN, FP):
    if (TN == 0 and FP == 0):
        return(float('NaN'))
    else:
        return(int(TN/(TN + FP)))

def getFNR(FN, TP):
    if (FN == 0 and TP == 0):
        return(float('NaN'))
    else:
        return(int(FN/(FN + TP)))

def getPPV(TP, FP):
    if (TP == 0 and FP == 0):
        return(float('NaN'))
    else:
        return(int(TP/(TP + FP)))

def getFDR(TP, FP):
    if (TP == 0 and FP == 0):
        return(float('NaN'))
    else:
        return(int(FP/(TP + FP)))

def getNPV(TN, FN):
    if (TN == 0 and FN == 0):
        return(float('NaN'))
    else:
        return(int(TN/(TN + FN)))

def getFOR(TN, FN):
    if (TN == 0 and FN == 0):
        return(float('NaN'))
    else:
        return(int(FN/(TN + FN)))

def getF1(PPV, TPR):
    if (isnan(PPV) or isnan(TPR)):
        return(float('NaN'))
    if (PPV == 0 and TPR == 0):
        return(float('NaN'))
    else:
        return(2*((PPV*TPR)/(PPV+TPR)))
        
def getPre(TP, FP, TN, FN):
    return((TP + FN)/(TP + FP + TN + FN))

def getACC(TP, FP, TN, FN):
    return((TP + TN)/(TP + FP + TN + FN))

def getLRP(TPR, FPR):
    if FPR == 0:
        return(float('NaN'))
    return(TPR/FPR)

def getLRN(FNR, TNR):
    if TNR == 0:
        return(float('NaN'))
    return(FNR/TNR)

def getDOR(LRP, LRN):
    if (LRN == 0):
        return(float('NaN'))
    else:
        return(LRP/LRN)

def binary_measures(out_row):
    TP  = out_row[7 ]
    FP  = out_row[8 ]
    TN  = out_row[9 ]
    FN  = out_row[10]
    TPR = getTPR(TP , FN)
    FPR = getFPR(FP , TN)
    TNR = getTNR(TN , FP)
    FNR = getFNR(FN , TP)
    PPV = getPPV(TP , FP)
    LRP = getLRP(TPR, FPR)
    LRN = getLRN(FNR, TNR)    
    
    out_row.append(TPR)
    out_row.append(FPR)
    out_row.append(getTNR(TN, FP))
    out_row.append(getFNR(FN, TP))
    out_row.append(PPV)
    out_row.append(getFDR(TP, FP))
    out_row.append(getNPV(TN, FN))
    out_row.append(getFOR(TN, FN))
    out_row.append(getF1(PPV, TPR))
    out_row.append(getPre(TP, FP, TN, FN))
    out_row.append(getACC(TP, FP, TN, FN))
    out_row.append(LRP)
    out_row.append(LRN)
    out_row.append(getDOR(LRP, LRN))
    
    return out_row
    
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
        csv_header = ['mut', 'rec', 'seqn', 'dualInf', 'rep', 'seq_name', 
                      'RC_seq', 'TP', 'FP', 'TN', 'FN', 'TPR', 'FPR', 'TNR', 
                      'FNR', 'PPV', 'FDR', 'NPV', 'FOR', 'F1', 'Pre', 'ACC', 
                      'LR+', 'LR-', 'DOR']
        writer.writerow(csv_header)
        counter = 0
        
        for index, sim_row in sim_bp.iterrows():
            
            counter += 1
            print("{}/{}".format(counter, len(sim_bp)))
            """ Iterate through each simulated sequence """
            out_row = []
            out_row.extend(parse_params_out(sim_row.params))
            out_row.extend([sim_row['seq']])
            
            if sim_seq_in_gc(sim_row, gc):
                """ GENCONV detected recombination at this param + seq """                
                bp_gc = bp_series_to_set(sim_row, gc)
                             
                if type(sim_row['breakpoints']) is float:
                    """ No breakpoints simulated """                    
                    rc_seq = 'FP'
                    out_row.append(rc_seq)
                    calc_yes_gc_no_sim(bp_gc, seq_length, out_row)
                    
                elif type(sim_row['breakpoints']) is set: 
                    """ Breakpoints simulated """
                    rc_seq = 'TP'
                    out_row.append(rc_seq)
                    calc_yes_gc_yes_sim(sim_row, bp_gc, seq_length, out_row)

            else:
                """ GENECONV detected to recombination at this param """
                rc_seq = rcseq_no_gc(sim_row['breakpoints'])
                out_row.append(rc_seq)
                calc_no_gc(sim_row, seq_length, out_row)
            
            binary_measures(out_row)
            writer.writerow(out_row) 
            

### Arguments -------------------- 
'''parser = argparse.ArgumentParser()
parser.add_argument("gc_dir", help = "path to dir containing geneconv output ()*.tab) files")
parser.add_argument("sim_bp", help = "simulated breakpoint file for each parameter and sequence")
args = parser.parse_args()
'''
### Main --------------------
#gc = gc_to_dict()
#sim_bp = prep_sim_file()
count_conditions(sim_bp, gc)
