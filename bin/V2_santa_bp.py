#!/usr/bin/env python3

import csv
import re
import glob
import os
    
# Append fasta files / filenames to list
os.chdir("/Users/13444841/Dropbox/Masters/03_results/out_190925/out_190917/S4_santa")
fileNames = []
print(" Reading simulated .fasta files...")
for file in glob.glob("**/*.fasta"):
    fileNames.append(file)

with open('V2_santa_bp.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['mut', 'rec', 'seqnum', 'dualInf', 'rep', 'seq', 'bps'])
    
    fileCounter = 0
    maxBPLen = 0 # To ensure correct number of columns
    
    for name in fileNames:
        fileCounter += 1
        print('[' + str(fileCounter) + '/' + str(len(fileNames)) + '] ' + name)
        # Parse file names for parameters
        params = re.sub('[a-z]+', '', name)
        params = params.split("_")
        params = params[1:6]
        with open(name) as file:
            for line in file:
                paramsNew = params.copy()
                if line.startswith('>'):
                    line = re.sub('>', '', line)
                    line = re.sub('\n', '', line)
                    if re.search(':', line):
                        line = line.split(':')
                        frequencyBP = len(line)
                        if frequencyBP > maxBPLen:
                            # Test max number of BPs for .csv columns
                            maxBPLen = frequencyBP
                            print("Max BP: " + str(maxBPLen))
                        paramsNew = paramsNew + line
                        writer.writerow(paramsNew)
                    else:
                        paramsNew.append(line)
                        writer.writerow(paramsNew)
print('Finished! Max BP in a single sequence: ' + str(maxBPLen))
                        
