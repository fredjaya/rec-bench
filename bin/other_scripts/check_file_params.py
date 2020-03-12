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
    if process_out in {"S4_santa", "div"}:
        for name in glob.glob("{}/*.fasta".format(path_to_dir)):
            file_names.append(name)

    if process_out == "B1_phi_profile":
        for name in glob.glob("{}/*.fasta_Profile.csv".format(path_to_dir)):
            file_names.append(name)

    if process_out == "B2_3seq":
        for name in glob.glob("{}/*.rec".format(path_to_dir)):
            file_names.append(name)

    if process_out == "B3_geneconv":
        for name in glob.glob("{}/*.tab".format(path_to_dir)):
            file_names.append(name)
    
    if process_out == "B3_geneconv":
        for name in glob.glob("{}/*.tab".format(path_to_dir)):
            file_names.append(name)
    
    if process_out == "B4_uchime":
        for name in glob.glob("{}/*.rc".format(path_to_dir)):
            file_names.append(name)

    else:
        print("fail to match process_out")
    return file_names

def params_regex(subject):
    p = re.sub(r'[a-z]+', '', subject)
    p = p.split("_")

    if args.process_out == "S4_santa":
        return p[4:9]

    if args.process_out == "div":
        return p[5:10]

    if args.process_out in {"B1_phi_profile", "B4_uchime"}:
        return p[7:12]

    if args.process_out in {"B2_3seq", "B3_geneconv"}:
        return p[6:11]  
    
    else:
        print("fail")

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

def count_occurrences(full_dict):
    c_mut = dict()
    c_rec = dict()
    c_seqn = dict()
    c_dualInf = dict()
    c_rep = dict()

    for param in full_dict.values():
        print(param)
        # https://stackoverflow.com/a/6582852
        c_mut[param['mut']] = c_mut.get(param['mut'], 0) + 1
        c_rec[param['rec']] = c_rec.get(param['rec'], 0) + 1
        c_seqn[param['seqn']] = c_seqn.get(param['seqn'], 0) + 1
        c_dualInf[param['dualInf']] = c_dualInf.get(param['dualInf'], 0) + 1
        c_rep[param['rep']] = c_rep.get(param['rep'], 0) + 1
        
    print("----- MUTATION RATE -----\n{}\n\
----- RECOMBINATION RATE -----\n{}\n\
----- SEQUENCE NUMBER -----\n{}\n\
----- DUAL INF RATE -----\n{}\n\
----- REPLICATE -----\n{}\n".format(c_mut, c_rec, c_seqn, c_dualInf, c_rep))

def main():
    intro(args.process_out, args.path_to_dir)
    file_names = get_file_names(args.path_to_dir, args.process_out)
    file_params = create_dict(file_names)
    count_occurrences(file_params)
    return

# Main ----------
main()
