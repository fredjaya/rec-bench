#!~/miniconda3/bin/python3.7 

import argparse
import re
import csv
import glob

### Arguments ----------
parser = argparse.ArgumentParser()
parser.add_argument("path_to_dir", help = "path to dir containing output files")
parser.add_argument("process_out", help = "process name from rec-bench/main.nf")
args = parser.parse_args()

### Functions ----------
def intro(process_out, path_to_dir):
    print("Checking output files for {}...".format(process_out))
    print("Reading files from {}...".format(path_to_dir))
    return

def get_file_names(path_to_dir, process_out):
    file_names = []
    if process_out == "S4_santa":
        for name in glob.glob("{}/*.fasta".format(path_to_dir)):
            file_names.append(name)
    return file_names

def params_regex(subject):
    p = re.sub(r'[a-z]+', '', subject)
    p = p.split("_")
    print(p)
    if args.process_out == "S4_santa":
        return p[4:9]

def list_to_dict(subject):
    param_names = ['mut', 'rec', 'seqn', 'dualInf', 'rep']
    param_vals  = params_regex(subject) 
    zipped_list = zip(param_names, param_vals)
    return dict(zipped_list)

def create_dict(file_names):
    full_dict = dict()
    n_index = 0
    for name in file_names:
        sub_dict = list_to_dict(name)
        full_dict[n_index] = sub_dict
        n_index += 1
    return full_dict     
 
def main():
    intro(args.process_out, args.path_to_dir)
    file_names = get_file_names(args.path_to_dir, args.process_out)
    file_params = create_dict(file_names)
    print(file_params)
    return

# Main ----------
main()
