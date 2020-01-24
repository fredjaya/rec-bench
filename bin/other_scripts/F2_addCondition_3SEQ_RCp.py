#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:35:39 2020

@author: Fred Jaya

Script to count conditions of 3SEQ predictions containing positive predictions

"""

import pandas as pd
import re
#import sys
import os

def parseSeqNum(fileName):
    n = re.findall('(?<=_n)\d+(?=_)', fileName)
    return(int(n[0]))

def readRecFile():
    print('Reading ' + currentParam)
    # Accounts for reading in files with multiple breakpoint columns
    fullRecPath = os.path.join(recPath, currentParam)
    recFile = pd.DataFrame([line.strip().split('\t') 
                for line in open(fullRecPath, 'r')])
    newHeader = recFile.iloc[0]
    recFile = recFile[1:]
    recFile.columns = newHeader
    return(recFile)
    
def getPredictedSeqs(simSeq, predictedRec):
    recAccNum = []
    seqID = re.findall('seq_\d+', str(list(predictedRec['C_ACCNUM'])))
    for i in seqID:
        if i not in recAccNum:
            recAccNum.append(i)
        elif i in recAccNum:
            print("ERROR: Duplicate sequences needs to be accounted for! (WIP)\n" +
                  simSeq['params'] + '\nTerminating at ' + i)
            return -1
    return(recAccNum)
    
def getPredictedBPs(simSeq, predictedRec): 
    breakpoints = []
    simRow = []
    # Subset matching seq
    for index, i in predictedRec.iterrows(): #list(predictedRec['C_ACCNUM']):
        if re.findall(simSeq['seq'], i['C_ACCNUM']):
            simRow = i
    if len(simRow) == 0:
        print('ERROR: Simulated sequences don\'t match predicted sequences!'
              '\n' + simSeq['params'] + '\n' + simSeq['seq'])
        return -1
    else:
        s = str(list(simRow.iloc[12:]))
        pattern = re.compile('\d+-\d+')
        matches = re.findall(pattern, s) 
        for i in matches:
            j = re.split('-', i)
            tempBP = list(range(int(j[0]), (int(j[1]) + 1)))
            for bp in tempBP:
                if bp not in breakpoints:
                    breakpoints.append(bp)
    return(breakpoints)
'''
print("Counting conditions for parameters where 3SEQ calculated negatives..." +
    "\nReading " + sys.argv[1] + "..." + '\nSequence length = ' + sys.argv[2])

simulatedBreakpoints = pd.read_csv(sys.argv[1])
seqLength = int(sys.argv[2])
recPath   = str(sys.argv[3])
'''

simulatedBreakpoints = pd.read_csv("/Users/13444841/Dropbox/Masters/02_working/2001_3seq_conditions/3seq_simBP_RCP.csv")
seqLength = 1680
recPath   = "/Users/13444841/Dropbox/Masters/02_working/2001_3seq_conditions/B2_3seq/RCp"

previousParam = None

for index, simSeq in simulatedBreakpoints.iterrows():

    currentParam = simSeq['params']
    
    if previousParam is None:
        predictedRec = readRecFile()
    elif currentParam is not previousParam:
        predictedRec = readRecFile()
    elif currentParam == previousParam:
        None
    
    previousParam = currentParam
    predictedSeqs = getPredictedSeqs(simSeq, predictedRec) 
    
    if pd.isna(simSeq['breakpoints']):
        #print("- No simulated breakpoints")
        
        if simSeq['seq'] not in predictedSeqs:
            #print("- No predicted breakpoints")
            TP = 0
            FP = 0
            TN = seqLength
            FN = 0
        
        elif simSeq['seq'] in predictedSeqs:
            #print("- Breakpoints predicted")
            predictedBreakpoints = getPredictedBPs(simSeq, predictedRec)
            TP = 0
            FP = len(predictedBreakpoints) # Only outputs first row of non-matching seq
            TN = seqLength - len(predictedBreakpoints)
            FN = 0
            
    elif re.findall(':', simSeq['breakpoints']):
       # print("- Breakpoints simulated")
        simBP = re.split(':', simSeq['breakpoints'])
        
        if simSeq['seq'] not in predictedSeqs:
            #print("- No breakpoints predicted")
            TP = 0
            FP = 0
            TN = seqLength - len(simBP)
            FN = len(simBP)
        
        elif simSeq['seq'] in predictedSeqs:
            #print("- Breakpoints predicted")
            falsePos = set(predictedBreakpoints) - set(simBP)
            falseNeg = set(simBP) - set(predictedBreakpoints)
            
            TP = len(predictedBreakpoints) - len(falsePos)
            FP = len(falsePos)
            TN = seqLength - len(predictedBreakpoints) - len(falsePos) - len(falsePos) - len(falseNeg)
            FN = len(falseNeg)
            TN = seqLength - TP - FP - FN
        
    simulatedBreakpoints.loc[index, 'TP'] = TP
    simulatedBreakpoints.loc[index, 'FP'] = FP
    simulatedBreakpoints.loc[index, 'TN'] = TN
    simulatedBreakpoints.loc[index, 'FN'] = FN

outputName = 'condition_3seq_simBP_RCP.csv'        
simulatedBreakpoints.to_csv(outputName, header = True, index = False,
                            na_rep = 'NA')
print("Written to " + outputName + "!")
