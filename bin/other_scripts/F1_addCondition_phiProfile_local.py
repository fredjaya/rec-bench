#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:54:57 2019

@author: Fred Jaya

Compares simulated breakpoints with detected breakpoints from PhiPack (Profile)
to determine the detected condition (i.e. FP/TP/FN/TN) across the sequence, per
window
"""

import pandas as pd
import re
import argparse
import os
import csv

# Functions ----------
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

def read_sim_bp(sim_path):
    sim_bp = pd.read_csv(sim_path)
    sim_bp['bps'] = bp_to_set(sim_bp)
    return sim_bp 

def read_phi(sim_row, phi_path):
    full_path = os.path.join(phi_path, sim_row['params'])
    phi_file = pd.read_csv(full_path, names = ['position', 'pval'])
    return phi_file

def parse_params(subject):
    r_alphas = re.compile(r'[a-z]+')
    r_rep = re.compile(r'(?<=\d)\.\.\d\.')

    p = re.sub(r_alphas, '', subject)
    p = re.sub(r_rep, '', p)
    p = p.split("_")
    return p[1:6]

def calc_no_sim(phi_row):
    if phi_row['pval'] < 0.05:
        return "FP"
    else:
        return "TN"

def missed_bps(sim_row):
    """ Get number of breakpoints that fall out of PHIs detection range """
    missed = 0
    for bp in sim_row['bps']:
        if (bp < 500 or bp > 1175):
            missed =+ 1
    return missed

def compare_detection(is_simulated, is_significant):
    if (is_simulated and is_significant):
        return "TP"
    elif (is_simulated and not is_significant):
        return "FN"
    elif (not is_simulated and is_significant):
        return "FP"
    elif (not is_simulated and not is_significant):
        return "TN"

def in_window(sim_row, phi_row):
    bp_in_window = []
    window_start = int(phi_row['position'])
    window_end = int(phi_row['position'] + 98)
    
    for bp in sim_row['bps']:
        if (window_start <= int(bp) <= window_end):
            bp_in_window.append(True)
        else: 
            bp_in_window.append(False)
            
    if True in bp_in_window:
        return True
    else:
        return False

def calc_yes_sim(sim_row, phi_row):
    is_significant = phi_row['pval'] < 0.05
    is_simulated = in_window(sim_row, phi_row)
    condition = compare_detection(is_simulated, is_significant)
    return condition

def make_outrow(params, phi_row, condition, missed):
    out_row = []
    out_row.extend(params)
    out_row.append(phi_row['position'])
    out_row.append(condition)
    out_row.append(missed)
    return out_row

def main(sim_bp, phi_path):
    with open("F1_profile_conditions.csv", 'w+') as csv_file:
        writer = csv.writer(csv_file)
        csv_header = ['mut', 'rec', 'seqn', 'dualInf', 'rep', 'position',
                      'condition', 'missed_bps']
        writer.writerow(csv_header)

        for index, sim_row in sim_bp.iterrows():
            """ Iterate through each parameter """
            phi_file = read_phi(sim_row, phi_path)
            params = parse_params(sim_row['params'])
            
            if type(sim_row['bps']) is float:
                missed = 0
                
                for index, phi_row in phi_file.iterrows():
                    condition = calc_no_sim(phi_row)
                    out_row = make_outrow(params, phi_row, condition, missed)
                    writer.writerow(out_row)
                    
            elif type(sim_row['bps']) is set:
                missed = missed_bps(sim_row)
                
                for index, phi_row in phi_file.iterrows():
                    condition = calc_yes_sim(sim_row, phi_row)
                    out_row = make_outrow(params, phi_row, condition, missed)
                    writer.writerow(out_row)

            else:
                print("fail")
                
    return
                
# Arguments ----------
"""parser = argparse.ArgumentParser()
parser.add_argument("sim_bp", help = "summarised simulated breakpoint file for each parameter")
parser.add_argument("phi_path", help = "path to Profile.csv outputs")
args = parser.parse_args()
"""
# Main ----------
sim_bp = read_sim_bp("/Users/13444841/Dropbox/Masters/03_results/2002_full_analysis/8_sim_bp/V3_sim_bp/V3_profile_sim_bp.csv")
phi_path = "/Users/13444841/Dropbox/Masters/03_results/2002_full_analysis/9_rec_path/F1_phi_profile"
main(sim_bp, phi_path)