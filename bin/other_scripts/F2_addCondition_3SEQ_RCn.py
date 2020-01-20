#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:16:57 2020

@author: Fred Jaya

Parses the .csv output from F0_simBP.Rmd to calculate the conditions for 3SEQ
analyses, where no recombinations were detected

"""

import pandas as pd
import re
import sys

def parseSeqNum(fileName):
    n = re.findall('(?<=_n)\d+(?=_)', fileName)
    return(int(n[0]))
        
print("Counting conditions for parameters where 3SEQ calculated negatives..." +
    "\nReading " + sys.argv[1] + "..." + '\nSequence length = ' + sys.argv[2])

simulatedBreakpoints = pd.read_csv(sys.argv[1])
seqLength = int(sys.argv[2])

for index, paramRow in simulatedBreakpoints.iterrows():
    
    seqNum = int(parseSeqNum(paramRow.loc['params']))
    totalBases = seqLength * seqNum
    
    if pd.isna(paramRow.loc['bps']):
        FN = 0
        TN = totalBases

    elif re.findall(':', paramRow.loc['bps']):
        FN = (len(re.findall(':', paramRow['bps']))) + 1
        TN = totalBases - FN
        print(FN)

    simulatedBreakpoints.loc[index, 'TP'] = 0
    simulatedBreakpoints.loc[index, 'FP'] = 0
    simulatedBreakpoints.loc[index, 'TN'] = TN
    simulatedBreakpoints.loc[index, 'TF'] = FN
    
    print('----------')
    print(simulatedBreakpoints.loc[index, 'params'] + '\nTN = ' + str(TN) + ' | FN = ' + str(FN))

outputName = "condition_" + sys.argv[1]
simulatedBreakpoints.to_csv(outputName, header = True, index = False, na_rep = 'NA')
print("Written to " + outputName + "!")
