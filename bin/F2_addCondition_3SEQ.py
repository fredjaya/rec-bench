#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:14:12 2020

@author: Fred Jaya
"""

import argparse
import pandas as pd
import re
import os
import csv
from math import isnan

# Arguments -----
parser = argparse.ArgumentParser()
parser.add_argument("sim_bp", help = "simulated breakpoint file (individual seqs")
parser.add_argument("rec_path", help = "path to 3SEQ output files (*.rec)")
args = parser.parse_args()

# Functions -----
def convert_bps(bp):
    if type(bp) is str:
        s = set()
        for i in re.findall('\d+', bp):
            s.add(int(i))
        return s

    elif type(bp) is float:
        return float('NaN')
    
def bp_to_set(sim_bp):
    d = []
    for index, sim_row in sim_bp.iterrows():
        bp = convert_bps(sim_row['bps']) 
        d.append(bp)
    return d
    
def parse_params(subject):
    r_alphas = re.compile(r'[a-z]+')
    r_rep = re.compile(r'(?<=\d)\.\.\d\.')
    
    p = re.sub(r_alphas, '', subject)
    p = re.sub(r_rep, '', p)
    p = p.split("_")
    return p[1:6]
    
def read_rec_file(current_param, rec_path):
    # Accounts for reading in files with multiple breakpoint columns                            
    #print("Reading {}".format(current_param))
    full_rec_path = os.path.join(rec_path, current_param)

    try: 
        rec_file = pd.DataFrame([line.strip().split('\t') 
                    for line in open(full_rec_path, 'r')])
        new_header = rec_file.iloc[0]
        rec_file = rec_file[1:]
        rec_file.columns = new_header
        
    except FileNotFoundError:
        """ Missing file due to sequences too similar for 3SEQ analysis """
        rec_file = None
    
    return rec_file

def iterate_rec_files(previous_param, current_param, seq, rec_path):
    """ Check if new 3SEQ file needs to be read """    
    if previous_param is None:
        return read_rec_file(current_param, rec_path)
    elif current_param is not previous_param:
        return read_rec_file(current_param, rec_path) 
    elif current_param == previous_param:
        None 

def match_seq(sim_row, predicted_rec):
    """ Check if sim seq is present in 3SEQ output """
    #https://stackoverflow.com/questions/57208954/select-rows-that-match-values-in-multiple-columns-in-pandas
    rec_row = predicted_rec[(predicted_rec['C_ACCNUM'] == sim_row['seq'])]
    return rec_row

def sim_seq_in_pred_rec(sim_row, predicted_rec):
    if match_seq(sim_row, predicted_rec).empty:
        return False
    else:
        return True
    
def predicted_bp_to_set(sim_row, predicted_rec):
    """ Get 3SEQ breakpoints that match simulated seq """
    breakpoints = set()
    rec_row = match_seq(sim_row, predicted_rec)
    
    s = str(list(rec_row.iloc[0, 12:]))
    pattern = re.compile(r'\d+-\d+')
    matches = re.findall(pattern, s)
      
    for i in matches:
        j = re.split('-', i)
        temp_bp = list(range(int(j[0]), (int(j[1]) + 1)))
        for bp in temp_bp:
            if bp not in breakpoints:
                breakpoints.add(bp)
                    
    return breakpoints

def rcseq_no_pred_rec(bp):
    if type(bp) is float:
        return "TN"
    if type(bp) is set:
        return "FN"
    
def bp_length(bp):
    if type(bp) is set:
        return len(bp)
    elif type(bp) is float:
        return 0
    
def append_out_row(TP, FP, TN, FN, out_row):
    out_row.append(TP)
    out_row.append(FP)
    out_row.append(TN)
    out_row.append(FN)
    return out_row

def calc_no_pred_rec(sim_row, seq_length, out_row):
    TP = 0
    FP = 0
    TN = seq_length - bp_length(sim_row['bps'])
    FN = bp_length(sim_row['bps'])
    return append_out_row(TP, FP, TN, FN, out_row)

def calc_yes_pred_rec_no_sim(bp_3seq, seq_length, out_row):
    TP = 0
    FP = bp_length(bp_3seq)
    TN = seq_length - bp_length(bp_3seq)
    FN = 0
    return append_out_row(TP, FP, TN, FN, out_row)

def true_pos(bp_sim, bp_3seq):
    i = bp_sim.intersection(bp_3seq)
    return len(i)

def false_pos(bp_sim, bp_3seq):
    d = bp_3seq.difference(bp_sim)
    return len(d)

def false_neg(bp_sim, bp_3seq):
    d = bp_sim.difference(bp_3seq)
    return len(d)

def true_neg(seq_length, TP, FP, FN):
    return seq_length - TP - FP - FN

def calc_yes_pred_rec_yes_sim(sim_row, bp_3seq, seq_length, out_row):
    TP = true_pos(sim_row['bps'], bp_3seq)
    FP = false_pos(sim_row['bps'], bp_3seq)
    FN = false_neg(sim_row['bps'], bp_3seq)
    TN = true_neg(seq_length, TP, FP, FN)
    return append_out_row(TP, FP, TN, FN, out_row)

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
    else:
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

def prep_sim_file():
    sim_bp = pd.read_csv(args.sim_bp)
    sim_bp['bps'] = bp_to_set(sim_bp)
    return sim_bp

def count_conditions(sim_bp, rec_path):
    seq_length = 1680
    """ Prep output .csv """
    with open("F2_3seq_conditions.csv", "w+") as csv_file:
        writer = csv.writer(csv_file)
        csv_header = ['mut', 'rec', 'seqn', 'dualInf', 'rep', 'seq_name',
                      'RC_seq', 'TP', 'FP', 'TN', 'FN', 'TPR', 'FPR', 'TNR',
                      'FNR', 'PPV', 'FDR', 'NPV', 'FOR', 'F1', 'Pre', 'ACC',
                      'LR+', 'LR-', 'DOR']
        writer.writerow(csv_header)

        previous_param = None
        
        for index, sim_row in sim_bp.iterrows():
            out_row = []
            
            """ Read in 3SEQ file """
            current_param = sim_row['params']
            predicted_rec = iterate_rec_files(previous_param, 
                                              current_param, 
                                              sim_row, 
                                              rec_path)
            
            """ Parse parameters """
            out_row.extend(parse_params(sim_row.params))
            out_row.extend([sim_row['seq']])
            
            if predicted_rec is None:
                """ Sequences too similar for 3SEQ analysis - return NaNs """
                out_row.extend(['nan'] * 19)

            elif predicted_rec.empty:
                """ 3SEQ detected no recombination at this param """
                rc_seq = rcseq_no_pred_rec(sim_row['bps'])
                out_row.append(rc_seq)
                calc_no_pred_rec(sim_row, seq_length, out_row)
                binary_measures(out_row)
            
            elif sim_seq_in_pred_rec(sim_row, predicted_rec):
                """ Recombination detected at this param; check if bps match"""
                bp_3seq = predicted_bp_to_set(sim_row, predicted_rec)
                print("Param: {}\n{}\nSim BP: {}\nSim Type: {}" \
                      .format(current_param, sim_row.seq, sim_row.bps, type(sim_row.bps)))

                if type(sim_row['bps']) is set:
                    """ Breakpoints simulated """
                    rc_seq = 'TP'
                    out_row.append(rc_seq)
                    calc_yes_pred_rec_yes_sim(
                            sim_row, bp_3seq, seq_length, out_row)
                    binary_measures(out_row)
                    
                elif type(sim_row['bps']) is float:
                    """ No breakpoints simulated """
                    rc_seq = 'FP'
                    out_row.append(rc_seq)
                    calc_yes_pred_rec_no_sim(bp_3seq, seq_length, out_row)
                    binary_measures(out_row)

            else:
                """ No breakpoints detected at this param """
                rc_seq = rcseq_no_pred_rec(sim_row['bps'])
                out_row.append(rc_seq)
                calc_no_pred_rec(sim_row, seq_length, out_row)
                binary_measures(out_row)
                
            #print(out_row)
            writer.writerow(out_row)
    return
# Main -----
rec_path = args.rec_path
sim_bp = prep_sim_file()
count_conditions(sim_bp, rec_path)
