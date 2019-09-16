#!/usr/bin/env python3

import csv
import re
import glob
import sys

# Read ${params.out} from nf
path = sys.argv[0]
path = str(path + "/*.fasta")

# Append fasta files / filenames to list
fileNames = []

for file in glob.glob(path):
    fileNames.append(file)
    #print(file)

with open('V1_bp_stats.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['mut', 'rec', 'seqL', 'dualInf', 'rep', 'bps'])

    for name in fileNames:
        # Parse file names for parameters
        params = re.sub('[a-z]+', '', name)
        params = params.split("_")
        params = params[1:]
        print(name)
        print(params)
        with open(name) as file:
            for line in file:
                paramsNew = params.copy()
                if line.startswith('>'):
                    #print(line)
                    if re.search(':', line):
                        line = line.split(':')
                        #print("colon found: " + str(line))
                        paramsNew.append(line)
                        #print(params)
                        print("YES BP: " +str(paramsNew))
                        writer.writerow(paramsNew)
                    else:
                        #print("no colon"  + line)
                        #params.append(line)
                        #print(params)

                    #print(params)
                    #end
                        paramsNew.append(line)
                        print("no bps: " + str(paramsNew))
                        writer.writerow(paramsNew)
