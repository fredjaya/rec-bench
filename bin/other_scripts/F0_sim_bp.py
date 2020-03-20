#!/usr/bin/env python3

"""
IN: V2_santa_bp.csv
OUT: sim_bp.csv per method
"""

# Packages ----------
import argparse
import pandas as pd
import re

# Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument("santa_bp",
    help = "path to 'V2_santa_bp.csv'")
parser.add_argument("process",
    help = "specify either: profile, 3seq, gc")
args = parser.parse_args()

# Functions ----------

def read_santa_bp(santa_bp):
    return pd.read_csv(santa_bp)

def clean_string(sim_bp):
    substitutions = [
        ('0.001', '0.0010'),
        ('0.01' , '0.010'),
        ('1e-07', '1.0E-7'),
        ('1e-06', '0.0000010'),
        ('1e-05', '0.000010'),
        ('1e-04', '0.00010')]
    
    for index, sim_row in sim_bp.iterrows(): 
        for query, subject in substitutions:
            print(type(sim_row.mut))
            sim_row['mut'] = re.sub(query, subject, sim_bp['mut'])
    return sim_bp 
# Main ----------

sim_bp = read_santa_bp(args.santa_bp)
clean_string(sim_bp)
print(sim_bp)
