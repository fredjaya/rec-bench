#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:24:50 2020

@author: Fred Jaya
"""

import csv
import os
import re

def is_significant(pval):
    return(float(pval) <= 0.05)
    
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
r = re.compile('(?<=\_n)\d+')
work_path  = "/Users/13444841/Dropbox/Masters/02_working/2002_phi_conditions/"
result_path = "/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/B1_phi_profile/"

sim_reader = csv.DictReader(open(os.path.join(work_path, "profile_simBP.csv")))

for sim_row in sim_reader:
    n_seq = int(re.findall(r, sim_row['params'])[0])
    profile_reader = csv.DictReader(open(
                         os.path.join(result_path, sim_row['params'])),
                         fieldnames = ('position', 'pval'))
    file_out = "{}out/condition_{}".format(work_path, sim_row['params'])
    
    with open(file_out, 'w') as csvfile:
            
        for profile_row in profile_reader:
            
            profile_row = dict(profile_row)
            profile_row['position'] = int(profile_row['position'])
            profile_row['pval'] = float(profile_row['pval'])
            
            conditions = {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0} 
            
            if sim_row['bps'] == 'NA':
                """No simulated breakpoints  """
                
                if float(profile_row['pval']) <= 0.05:
                    """Signficant recombination detected  """
                    conditions['TN'] = (window_size*n_seq)
                    break
                else:
                    """No significant recombination detected  """
                    conditions['FN'] = (window_size*n_seq)
                    
                break
            
            else:
                """Breakpoints are simulated in this replicate  """
                window_start = int(profile_row['position'])
                window_end   = int(profile_row['position']) + 99
                
                sim_bp = get_sim_BP_counts(sim_row)
                
                """Check if breakpoints are within the window  """
                for i, (key, value) in enumerate(sim_bp.items()):
                    if window_start <= value['bps'] <= window_end:
                        """Breakpoint is within window  """
                        if is_significant(profile_row['pval']):
                            """Window is significant for recombination  """
                            conditions['TP'] = conditions['TP'] + value['count']
                            break
                        
                        else:
                            """ No significant recombination detected  """
                            conditions['FN'] = conditions['FN'] + value['count']
                            
                        break
                    
                """Complete conditions  """
                if is_significant(profile_row['pval']):
                    conditions['FP'] = (window_size*n_seq) - conditions['TP']
                    break
                else:
                    conditions['TN'] = (window_size*n_seq) - conditions['FN']
                
                """Write window conditions per window """
                profile_row.update(conditions)
                writer = csv.DictWriter(csvfile, fieldnames = profile_row.keys())
                writer.writerow(profile_row)
        print(sim_row['params'])
                    
                