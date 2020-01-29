#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:54:57 2019

@author: Fred Jaya

Compares simulated breakpoints with detected breakpoints from PhiPack (Profile)
to determine the detected condition (i.e. FP/TP/FN/TN) across the sequence, per
window

TODO:
    * Refactor bpPerWindow into function
"""

import pandas as pd
import re
from math import isnan
import sys

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

simulatedBreakpoints = "~/Dro"

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
