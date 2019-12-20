#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:54:57 2019

@author: Fred Jaya

Compares simulated breakpoints with detected breakpoints from PhiPack (Profile)
to determine the detected condition (i.e. FP/TP/FN/TN) across the sequence, per
window

Currently works for all sequences within a parameter/rep.

TODO:
    * Refactor bpPerWindow into function
    * Add command line conditions/help
"""

import pandas as pd
import re
from math import isnan
import sys

"""
# single BP
simulatedBreakpoints = pd.read_csv("sim_bp_singleSeq_oneBP.csv")
phiProfile           = pd.read_csv("msa_m0.000010_rc0.010_n100_dual1_rep2.fasta_Profile.csv",
                                   names = ['position', 'pvalue'])

# multi BP
simulatedBreakpoints = pd.read_csv("sim_bp_singleSeq_multiBP.csv")
phiProfile           = pd.read_csv("msa_m0.000010_rc0.010_n100_dual1_rep2.fasta_Profile.csv",
                                   names = ['position', 'pvalue'])

# no BP
simulatedBreakpoints = pd.read_csv("sim_bp_singleSeq_noBP.csv")
phiProfile           = pd.read_csv("msa_m0.000010_rc1.0E-7_n100_dual1_rep1.fasta_Profile.csv",
                                   names = ['position', 'pvalue'])

# all sequences in a rep
simulatedBreakpoints = pd.read_csv("sim_bp_allSeqsInRep.csv")
phiProfile           = pd.read_csv("msa_m0.000010_rc0.010_n100_dual1_rep2.fasta_Profile.csv",
                                   names = ['position', 'pvalue'])
"""

# Functions
def getSignificance(obsPval):
    return(obsPval < 0.05)
    
def getCondition(isSimulated, isSignificant):
    if isSimulated:
        if isSignificant:
            condition = "TP"
        elif not isSignificant:
            condition = "FN"
    elif not isSimulated:
        if isSignificant:
            condition = "FP"
        elif not isSignificant:
            condition = "TN"
    return(condition)

# Set log
log = open("phi_condition.log", "w")
sys.stdout = log
print("Simulated breakpoint file: " + sys.argv[1] +
      "\nPhiPack Profile.csv: " + sys.argv[2])

# Read inputs - simulated breakpoints and detected files
#os.chdir("/Users/13444841/Dropbox/Masters/02_working/1912_precision_recall/191216_phiprofile/")  
simulatedBreakpoints = pd.read_csv(sys.argv[1])
phiProfile           = pd.read_csv(sys.argv[2], names = ['position', 'pvalue'])

print("==========\nCalculating conditions for all sequences at " +
      simulatedBreakpoints.loc[0]['params'] + "\n==========")

for index, simRow in simulatedBreakpoints.iterrows():
    print("-- " + simRow['seq'] + " --")
    # Check if BPs were simulated
    if not isinstance(simRow['breakpoints'], str):
        isnan(simRow['breakpoints'])
        
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
            phiProfile.loc[index, "cond_" +
                           str(simRow['seq'])] = condition
            print("At window " + str(windowStart) + "-" + str(windowEnd) +
                  "\nSimulated breakpoint = NA" + 
                  "\nSignificant p-value  = " + str(isSignificant) + 
                  "\nCONDITION = " + condition + "\n----------")
        
    else:
        # Create list of  breakpoints if multiple BPs
        multipleSimBP = []
        if re.findall(':', str(simRow['breakpoints'])):
            multipleSimBP  = True
            breakpointList = re.split(':', simRow['breakpoints'])
        else:
            multipleSimBP  = False
            breakpointList = simRow['breakpoints']
            
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
            phiProfile.loc[index, "cond_" +
                           str(simRow['seq'])] = condition
            print("At window " + str(windowStart) + "-" + str(windowEnd) +
                  "\nSimulated breakpoint = " + str(isSimulated) + 
                  "\nSignificant p-value  = " + str(isSignificant) + 
                  "\nCONDITION = " + condition + "\n----------")
        
# Write to .csv
outputName = "condition_" + simulatedBreakpoints.iloc[0]['params']
phiProfile.to_csv(outputName, header = True, index = False)
print("Writing to " + outputName)