#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:54:57 2019

@author: Fred Jaya

Compares simulated breakpoints with detected breakpoints from PhiPack (Profile)
to determine the detected condition (i.e. FP/TP/FN/TN) across the sequence, per
window

TODO:
    * Add full path to file name
    * Refactor bpPerWindow into function
"""

import argparse
import csv
import os
import pandas as pd
import re
from math import isnan
import sys

# Functions


def get_condition(is_simulated, is_significant):
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

def concat_full_path(sim_row, path):
    """
    Append full path to read in individual Profile.csvs
    """
    return os.path.join(path, sim_row[0])

def sim_bps_exist(bps):
    if bps == 'NA':
        return False
    else:
        return True
    return

def get_significance(pval):
    return(pval <= 0.05)

def process_no_simbp(phi_reader):
    """
    Iterate through windows to determine conditions 
    when no breakpoints are simulated
    """
    is_simulated = False

    for phi_row in phi_reader:
        window_pval = float(phi_row[1])
        is_significant = get_significance(window_pval)
        condition = get_condition(is_simulated, is_significant)
        print(condition)
    """
        # Set detection window size
        windowStart = int(phiRow[0])
        windowEnd   = int(phiRow[0] + 99)

        # Check for significance within that window region and determine cond.
        isSignificant = getSignificance(phiRow[1])
        condition = getCondition(isSimulated, isSignificant)

        # Write condition to column in Profile.csv
        phiProfile.loc[index, "cond"] = condition
        print("At window " + str(windowStart) + "-" + str(windowEnd) +
              "\nSimulated breakpoints = " + simulatedBreakpoints +
              "\nSignificant p-value  = " + str(isSignificant) +
              "\nCONDITION = " + condition + "\n----------")
    """
    return

def process_profile_row(sim_row, path):
    """
    Calculate conditions per row in V3_profile_sim_bp.csv
    """
    full_path = concat_full_path(sim_row, path)
    
    with open(full_path, 'r+') as phi_file:
        phi_reader = csv.reader(phi_file)
        
        if sim_bps_exist(sim_row[1]):
            print("Simulated breakpoints")
        else:
            process_no_simbp(phi_reader)
    return

def profile_conditions(sim_bp, path):
    """
    For each line in V3_profile_sim_bp.csv, read in file and calculate conditions
    """
    with open("F1_profile_conditions.csv", 'w+') as csv_file:
        writer = csv.writer(csv_file)
        csv_header = ['mut', 'rec', 'seqn', 'dualInf', 'rep',
                        'position', 'condition', 'missed_bps']
        writer.writerow(csv_header)

        with open (sim_bp, 'r+') as f:
            sim_bp_reader = csv.reader(f)
            next(sim_bp_reader, None) # Skip header ['params', 'bps']
            
            for sim_row in sim_bp_reader:
                process_profile_row(sim_row, path)
                """
# Check if BPs were simulated
if simulatedBreakpoints == 'NA':

    isSimulated = False

    # Iterate through Profile.csv positions to determine condition
    for index, phiRow in phiProfile.iterrows():
        condition   = []

        # Set detection window size
        windowStart = int(phiRow[0])
        windowEnd   = int(phiRow[0] + 99)

        # Check for significance within that window region and determine cond.
        isSignificant = getSignificance(phiRow[1])
        condition = getCondition(isSimulated, isSignificant)

        # Write condition to column in Profile.csv
        phiProfile.loc[index, "cond"] = condition
        print("At window " + str(windowStart) + "-" + str(windowEnd) +
              "\nSimulated breakpoints = " + simulatedBreakpoints +
              "\nSignificant p-value  = " + str(isSignificant) +
              "\nCONDITION = " + condition + "\n----------")

else:
    # Create list of  breakpoints if multiple BPs
    multipleSimBP = []
    if re.findall(':', str(simulatedBreakpoints)):
        multipleSimBP  = True
        breakpointList = re.split(':', simulatedBreakpoints)
    else:
        multipleSimBP  = False
        breakpointList = simulatedBreakpoints

    # Iterate through Profile.csv positions to determine condition
    for index, phiRow in phiProfile.iterrows():
        condition     = []
        isSignificant = []
        isSimulated   = []

        # Set detection window size
        windowStart = int(phiRow[0])
        windowEnd   = int(phiRow[0] + 99)

        # Check if any breakpoints were simulated within each window position
        bpPerWindow = []
        if multipleSimBP:
            for bp in breakpointList:
                if windowStart <= int(bp) <= windowEnd:
                    bpPerWindow.append(True)
                else:
                    bpPerWindow.append(False)

        elif not multipleSimBP:
            bp = breakpointList
            if windowStart <= int(bp) <= windowEnd:
                bpPerWindow.append(True)
            else:
                bpPerWindow.append(False)

        if True in bpPerWindow:
            isSimulated = True
        else:
            isSimulated = False

        # Check for significance within that window region and determine cond.
        isSignificant = getSignificance(phiRow[1])
        condition = getCondition(isSimulated, isSignificant)

        # Write condition to column in Profile.csv
        phiProfile.loc[index, "cond"] = condition
        print("At window " + str(windowStart) + "-" + str(windowEnd) +
              "\nSimulated breakpoint = " + str(isSimulated) +
              "\nSignificant p-value  = " + str(isSignificant) +
              "\nCONDITION = " + condition + "\n----------")

# Write to .csv
outputName = "condition_" + sys.argv[1]
phiProfile.to_csv(outputName, header = True, index = False)
print("Writing to " + outputName)
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sim_bp", help = "simulated breakpoint file for each parameter and sequence (V3_profile_sim_bp.csv")
    parser.add_argument("profile_path", help = "path to *Profile.csvs")
    args = parser.parse_args()

    profile_conditions(args.sim_bp, args.profile_path) 
