#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:54:57 2019

@author: Fred Jaya

Compares simulated breakpoints with detected breakpoints from PhiPack (Profile)
to determine the detected condition (i.e. FP/TP/FN/TN) across the sequence, per
window. 

Previously, this script was run only for one Profile.csv via nextflow.

Now it is run via the command-line, processing all Profile.csvs in a directory.
"""

import argparse
import csv
import os
import pandas as pd
import re
from math import isnan
import sys

# Functions
def set_csv_fieldsize():
    """
    In case there are hundred of breakpoints in the .csv per param
    """
    csv.field_size_limit(999999)
    return

def get_condition(is_simulated, is_significant):
    """
    Determine the condition of a detection window based on the presence
    of simulated breakpoints within the window and if p-value is significant
    """
    if is_simulated:
        if is_significant:
            condition = "TP"
        elif not is_significant:
            condition = "FN"
    elif not is_simulated:
        if is_significant:
            condition = "FP"
        elif not is_significant:
            condition = "TN"
    return condition

def concat_full_path(path, file_name):
    """
    Append full path to read in individual Profile.csvs
    """
    return os.path.join(path, file_name)

def sim_bps_exist(bps):
    if bps == 'NA':
        return False
    else:
        return True
    return

def get_significance(pval):
    return(pval <= 0.05)

def write_output_row(params, position, condition, writer):
    """
    Write a complete .csv row with parsed params, position of detection window,
    and the condition of the detection in the window
    """
    out_row = []
    out_row.extend(params)
    out_row.append(position)
    out_row.append(condition)
    writer.writerow(out_row)
    return

def process_no_simbp(phi_reader, params, writer):
    """
    Iterate through windows to determine conditions 
    when no breakpoints are simulated
    """
    is_simulated = False

    for phi_row in phi_reader:
        position = int(phi_row[0])
        window_pval = float(phi_row[1])
    
        is_significant = get_significance(window_pval)
        condition = get_condition(is_simulated, is_significant)
    
        write_output_row(params, position, condition, writer)   
    return

def check_simbp_in_window(position, bp):
    """
    Determine if simulated breakpoints are present within a window
    Default Profile window size == 1000 nt
    """
    window_start = position - 499
    window_end = position + 500
    
    if window_start <= int(bp) <= window_end:
        return True
    else:
        return False

def iterate_bp(position, breakpoints):
    """
    Iterate through all simulated breakpoints to determine 
    if any fall within the detection window
    """
    for bp in breakpoints:
        if check_simbp_in_window(position, bp):
            return True
        else:
            pass
    return False
    
def process_with_simbp(phi_reader, breakpoints, params, writer):
    """
    Iterate through windows to determine conditions
    when breakpoints are simulated
    """
    for phi_row in phi_reader:
        position = int(phi_row[0])
        window_pval = float(phi_row[1])
        
        is_significant = get_significance(window_pval)
        is_simulated = iterate_bp(position, breakpoints)
        condition = get_condition(is_simulated, is_significant)
        
        write_output_row(params, position, condition, writer)   
    return

def parse_params(file_name):
    """
    Extract the simulation parameters from file names
    """
    p = re.sub(r'^.*(?=msa)', '', file_name)
    p = re.sub(r'[a-z]+', '', p)
    p = p.split('_')
    return p[1:6]

def process_profile_row(sim_row, path, writer):
    """
    Calculate conditions per row in V3_profile_sim_bp.csv
    """
    full_path = concat_full_path(path, sim_row[0])
    params = parse_params(sim_row[0])
    breakpoints = sim_row[1]
    
    try:
        with open(full_path, 'r+') as phi_file:
            phi_reader = csv.reader(phi_file)
            
            if sim_bps_exist(breakpoints):
                breakpoints = breakpoints.split(":")
                process_with_simbp(phi_reader, breakpoints, params, writer) 
            else:
                process_no_simbp(phi_reader, params, writer)
    
    except FileNotFoundError:
        print("File not found:", sim_row[0])

    return


def profile_conditions(sim_bp, path):
    """
    For each line in V3_profile_sim_bp.csv, read in file and calculate conditions
    """
    with open("F1_profile_conditions.csv", 'w+') as csv_file:
        writer = csv.writer(csv_file)
        csv_header = ['mut', 'rec', 'seqn', 'dualInf', 'rep',
                        'position', 'condition']
        writer.writerow(csv_header)

        with open (sim_bp, 'r+') as f:
            sim_bp_reader = csv.reader(f)
            next(sim_bp_reader, None) # Skip header ['params', 'bps']
            
            for sim_row in sim_bp_reader:
                process_profile_row(sim_row, path, writer)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sim_bp", help = "simulated breakpoint file for each parameter and sequence (V3_profile_sim_bp.csv")
    parser.add_argument("profile_path", help = "path to *Profile.csvs")
    args = parser.parse_args()
    
    set_csv_fieldsize()
    profile_conditions(args.sim_bp, args.profile_path) 
