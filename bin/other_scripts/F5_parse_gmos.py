#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:31:20 2020

@author: 13444841
"""

import argparse
import glob
import re
import csv

# Functions ----------
def get_file_names(gmos_dir):
    file_names = []
    for name in glob.glob("{}*.txt".format(gmos_dir)):
        file_names.append(name)
    return file_names

def parse_params(name):
    """ Split file name into individual parameters """
    p = re.sub('^.*(?=msa)', '', name)
    p = re.sub('[a-z]+', '', p) 
    p = p.split("_")
    return p[1:6]

def colnames():
    column_names = ['mut', 'rec', 'seqLen', 'dualInf', 'rep', \
                    'q_seq', 'q_start_bp', 'q_end_bp', 'sig', \
                    'end_bp2', 'score', 'evalue', 's_short', \
                    's_full', 's_start_bp', 's_end_bp', 'strand_dir']
    return column_names

def query_row(line):
    query = re.findall(r'(?<=\)\s).*(?=\s\-)', line)
    return query
    
def gmos_to_csv(file_names):
    with open("F5_gmos_summarised.csv", "w+") as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        writer.writerow(colnames())

        for f in file_names:
            
            with open(f, 'r+') as gmos:
                out_row = parse_params(f)
                query = []
                subject = []
                
                for line in gmos:
                    if re.findall('^$', line):
                        pass
                    
                    elif re.findall('^-', line):
                        query = query_row(line)
                    
                    elif re.findall('\s', line):
                        subject = line.split()
                        out_row.extend(query + subject)
                        writer.writerow(out_row)          
                        out_row = parse_params(f)
    return

# Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument("gmos", help = "path to gmos output files (*_gmos.txt)")
args = parser.parse_args()
"""

# Main ----------
gmos_path = "/Users/13444841/Dropbox/Masters/03_results/2002_full_analysis/4_bm_n1000/B5_gmos/"
file_names = get_file_names(gmos_path)
gmos_to_csv(file_names)