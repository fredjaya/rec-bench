#!/usr/bin/python3

import glob
import csv
import argparse
import re
import os

# Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument("sim_path", 
    help = "path to dir containing simulation outputs '/S4_santa'")
args = parser.parse_args()

# Functions ----------
def set_path(sim_path):
    return os.path.join(sim_path, "stats_*.csv")

def get_file_names(joined_path):
    file_names = []
    print("Reading santa stats files ...")
    for file in glob.glob(joined_path):
        file_names.append(file)
    return file_names

def parse_sims(sim_file):
    """ Parse file name for params """
    p = re.sub('^.*(?=stats)', '', sim_file) 
    p = re.sub('stats_', '', p)
    p = re.sub('.csv', '', p)
    p = re.sub('[a-z]', '', p)
    p = p.split('_')
    
    """ Read sim outputs for population stats """ 
    f = open(sim_file, 'r').read()
    f = f.split('\n')
    f = f[1].split(',')
    
    return p + f
    
def concat_sim_outputs(file_names):
    with open('V1_santa_stats.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        header = (['mut', 'rec', 'seqLen', 'dualInf', 'rep', 'generation',
                   'population_size', 'mean_diversity', 'max_diversity',
                   'min_fitness', 'mean_fitness', 'max_fitness', 
                   'max_frequency', 'mean_distance'])
        writer.writerow(header) 
        for sim_file in file_names:
            out_row = parse_sims(sim_file)
            writer.writerow(out_row)
    return

# Main ----------
joined_path = set_path(args.sim_path)
file_names = get_file_names(joined_path)
concat_sim_outputs(file_names)
