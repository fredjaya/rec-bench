#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:34:52 2020

@author: Fred Jaya

Calculates scores (i.e. precision, recall etc.) based on parsed phi condition
outputs.
"""

import sys
import pandas as pd
import glob
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

#path = sys.argv[1]
#os.chdir(path)

fileNames = []

print("Reading PhiPack (Profile) window conditions...")

for names in glob.glob("F1_phi_profile/*.csv"):
    fileNames.append(names)

with open('F1_phi_profile_fscore.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    header = ['mut', 'rec', 'seqn', 'dualInf', 'rep', 'TP', 'FP', 'TN', 'FN',
    'TPR', 'FPR', 'TNR', 'FNR', 'PPV', 'FDR', 'NPV', 'FOR', 'F1', 'Pre', 'ACC',
    'LR+', 'LR-', 'DOR']
    writer.writerow(header)

    for file in fileNames:
        print("Calculating " + file + " ...")
        phiCond = pd.read_csv(file)

        # Parse parameters
        params = re.sub('[a-z]+', '', file)
        params = params.split("_")
        params = params[4:9]

        # Count conditions
        TP = int(phiCond.loc[phiCond.cond == 'TP' , 'cond'].count())
        FP = int(phiCond.loc[phiCond.cond == 'FP' , 'cond'].count())
        TN = int(phiCond.loc[phiCond.cond == 'TN' , 'cond'].count())
        FN = int(phiCond.loc[phiCond.cond == 'FN' , 'cond'].count())

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
