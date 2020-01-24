#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:34:52 2020

@author: Fred Jaya

Calculates scores (i.e. precision, recall etc.) based on parsed phi condition
outputs.
"""

import pandas as pd
import csv
import re
import math

# True conditions as denominator
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

# Predicted conditions as denominator
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

# F1 score
def getF1(PPV, TPR):
    if (math.isnan(PPV) or math.isnan(TPR)):
        return(float('NaN'))
    if (PPV == 0 and TPR == 0):
        return(float('NaN'))
    else:
        return(2*((PPV*TPR)/(PPV+TPR)))

# Whole population metrics
def getPre(TP, FP, TN, FN):
    return((TP + FN)/(TP + FP + TN + FN))

def getACC(TP, FP, TN, FN):
    return((TP + TN)/(TP + FP + TN + FN))

# Likelihood ratios
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

# Write .csv
def writeMetrics(RC):

    writer = csv.writer(csvfile, delimiter = ',')
    header = ['mut', 'rec', 'seqn', 'dualInf', 'rep', 'TP', 'FP', 'TN', 'FN',
    'TPR', 'FPR', 'TNR', 'FNR', 'PPV', 'FDR', 'NPV', 'FOR', 'F1', 'Pre', 'ACC',
    'LR+', 'LR-', 'DOR']
    writer.writerow(header)

    for index, paramRow in RC.iterrows():
        print(paramRow)

        # Parse parameters
        params = re.sub('[a-z]+', '', paramRow.params)
        params = re.sub('\.\.3\.', '', params)
        params = params.split("_")
        params = params[1:6]

        # Set conditions
        TP = paramRow.TP
        FP = paramRow.FP
        TN = paramRow.TN
        FN = paramRow.FN

        # Rate of each condition based on total true conditions
        TPR = getTPR(TP, FN)
        FPR = getFPR(FP, TN)
        TNR = getTNR(TN, FP)
        FNR = getFNR(FN, TP)

        # Rate of each condition based on predicted conditions
        PPV = getPPV(TP, FP)
        NPV = getNPV(TP, FP)
        FDR = getFDR(TN, FN)
        FOR = getPPV(TN, FN)

        # F1 score
        F1  = getF1(PPV, TPR)

        # Total population measurements
        Pre = getPre(TP, FP, TN, FN)
        ACC = getACC(TP, FP, TN, FN)

        # Likelihood ratios
        LRP = getLRP(TPR, FPR)
        LRN = getLRN(FNR, TNR)
        DOR = getDOR(LRP, LRN)

        # Write row
        writer.writerow(params + [TP, FP, TN, FN, TPR, FPR, TNR, FNR, PPV, FDR, NPV, FOR, F1, Pre, ACC, LRP, LRN, DOR])

RCp = pd.read_csv("/Users/13444841/Dropbox/Masters/02_working/2001_3seq_conditions/condition_3seq_simBP_RCP.csv")
RCn = pd.read_csv("/Users/13444841/Dropbox/Masters/02_working/2001_3seq_conditions/condition_3seq_simBP_RCN.csv")

print('Reading 3SEQ window conditions')

# Calculate metrics for RCn
with open('F2_3SEQ_fscore_RCn.csv', 'w+') as csvfile:
    writeMetrics(RCn)

# Calculate metrics for RCp
with open('F2_3SEQ_fscore_RCp.csv', 'w+') as csvfile:
    writeMetrics(RCp)
