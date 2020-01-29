#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:24:50 2020

@author: Fred Jaya
"""

import csv
import os
import re

def getSignificance(pval):
    return(pval < 0.05)
    
def get_sim_BP_counts(sim_row):
    d = {}
    if re.findall(':', sim_row['bps']):
        """For multiple bps """
        sim_bps = sim_row['bps'].split(":")
        unique_bps = set(sim_bps)
        dict_index = 0
        
        for i in unique_bps:
            """ Get counts per unique breakpoint
            
            Iterate through unique breakpoints and create a dictionary of
            counts per breakpoint. Counts to be used to multiple conditions.  
            """
            ind_count = sim_bps.count(i)
            d[dict_index] = {"bps": int(i), "count": int(ind_count)} 
            dict_index += 1            
                
    else:
        """For only one breakpoint """
        j = int(sim_row['bps'])
        d[0] = {"bps": int(j), "count": 1}
    
    return(d)        
    
window_size = 100

sim_reader = csv.DictReader(open(
        "/Users/13444841/Dropbox/Masters/02_working/2002_phi_conditions/profile_simBP.csv"))

for sim_row in sim_reader:
    path = os.path.join(
        "/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B1_phi_profile/",
        sim_row['params'])
    
    profile_reader = csv.DictReader(open(path), 
                                    fieldnames = ('position', 'bp'))
    
    for profile_row in profile_reader:
        if sim_row['bps'] == 'NA':
            """No simulated breakpoints  """
            
            if float(profile_row['bp']) < 0.05:
                """No signficant recombination detected  """
                TP = 0
                FP = 0
                TN = window_size
                FN = 0
                break
            
            else:
                """Significant recombination detected  """
                TP = 0
                FP = window_size
                TN = 0
                FN = 0
                break
        
        else:
            """Breakpoints are simulated  """
            window_start = int(profile_row['position'])
            window_end   = int(profile_row['position']) + 99
            
            print(sim_row['bps'])
            print(get_sim_BP_counts(sim_row))