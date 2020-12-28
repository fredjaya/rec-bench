#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:29:03 2020

@author: Fred Jaya
"""

import pandas as pd
import re

def match_breakpoints(bp):
    if type(bp) is str:
        s = set()
        for i in re.findall('\d+', bp):
            s.add(int(i))
        return s
    elif type(bp) is float:
        return float('NaN')

def bp_to_set(sim_bp):
    d = []
    for index, sim_row in sim_bp.iterrows():
        d.append(match_breakpoints(sim_row['bps']))
    return d

def prep_sim_file(sim_path):
    sim_bp = pd.read_csv(sim_path)
    sim_bp['bps'] = bp_to_set(sim_bp)
    return sim_bp

sim_bp = prep_sim_file("/Users/13444841/Dropbox/Masters/02_working/2003_geneconv_conditions/V3_gc_sim_bp.csv")

