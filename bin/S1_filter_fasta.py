# This script prepares .fasta files for analysis in santa-sim and UCHIME.
# Both these programs cannot process sequences containing "-".

#!/usr/bin/env python3

import sys
import re
from matplotlib import pyplot as plt

## Check argument ##
if len(sys.argv) < 2:
    print("Please specify a .fasta file!")
    exit()
if len(sys.argv) > 2:
    print("Too many arguments! Please specify one .fasta file.")
    exit()
if len(sys.argv) == 2:
    data = sys.argv[1]
    sys.stdout = open(data + '_log.txt','wt')
    print("||\n"
          "||  Reading", data, "...")

## Define functions and preliminary variables ##
def seqLenHist( seqLength, maxseq, minseq, x ):
    # Plot freq hist of sequence length based on range
    if (maxseq - minseq) <= 1:
        print("||  All sequences are", maxseq, "bp\n||")
    if (maxseq - minseq) > 1:
        print("||   Longest sequence is %i" % maxseq, "\n"
              "||  Shortest sequence is %i" % minseq, "\n"
              "||  Plotting sequence length frequencies to seqLengthFHist" + x + ".png...\n||")
        plt.hist(seqLength, bins = range(minseq, maxseq + 1, 1), align = 'right')
        plt.savefig("seqLengthFHist"+ x + ".png")

# Set string for I/O files
data_m = data + "_m" # [m]odified sequence names
data_n = data + "_n" # [n]o gaps in sequences

# Set list for sequence lengths
seqLengthA = []
seqLengthB = []

## Inspect and modify .fasta files ##
with open(data, "r") as f_in:
    # Replace characters in header with '_' for downstream analyses
    f_out_m = open(data_m, "w")
    for f_in in f_in:
        f_out_m.write(re.sub('([()\/])', '_', f_in))

with open(data_m) as f_out_m:
    # Delete gaps from sequences
    f_out_n = open(data_n, "w")
    f_out_m = f_out_m.readlines()
    for line in f_out_m:
        if line.startswith('>'):
            f_out_n.write(line)
        if not line.startswith('>'):
            seqLengthA.append(len(line))
            f_out_n.write(re.sub('-', '', line))

seqNum = len(seqLengthA)
print("||  Total of " + str(seqNum) + " sequences")

with open(data_n) as f_out_n:
    # Find the max sequence length of gapless alignment
    f_out_n = f_out_n.readlines()
    for line in f_out_n:
        if not line.startswith('>'):
            seqLengthB.append(len(line))

# Plot sequence length histogram of original input alignment
maxseqA = max(seqLengthA)-1
minseqA = min(seqLengthA)-1
seqLenHist(seqLengthA, maxseqA, minseqA, "A" )

# Plot histogram after gaps have been removed
print("||  Removing all gaps in", data, "...\n||")
maxseqB = max(seqLengthB)-1
minseqB = min(seqLengthB)-1
seqLenHist(seqLengthB, maxseqB, minseqB, "B" )

# Remove sequences that =/= max(seqLength) and create filtered .fa files
# From: https://www.biostars.org/p/352679/
seq = {}
longSeq = []
shortSeq = []

with open(data_n, "r") as f_out_n:
    for line in f_out_n:
        line = line.rstrip()
        if (line[0] == '>'):
            header = line
            seq[header] = ""
        else:
            seqInd = line
            seq[header] += seqInd

# Test
if (len(seq) != seqNum):
    print("*** Sequence numbers don't add up! ***")
    exit()

# Append sequences based on seq length
for header in seq.keys():
    if (len(seq[header]) == maxseqB):
        longSeq.append(header)
    else:
        shortSeq.append(header)

data_n_f = data_n + "_filtered"
data_n_r = data_n + "_removed"

# Write good sequences
with open(data_n_f, "w") as good_out:
    for header in longSeq:
        good_out.write("{}\n{}\n"
                       .format(header, seq[header]))

# Write bad sequences
with open(data_n_r, "w") as bad_out:
    for header in shortSeq:
        bad_out.write("{}\n{}\n"
                       .format(header, seq[header]))

longSeqNum = len(longSeq)
shortSeqNum = len(shortSeq)
longSeqPerc = (longSeqNum/seqNum)*100

# Test
if (longSeqNum + shortSeqNum != seqNum):
    print("*** Sequence numbers don't add up! ***")
    exit()

print("||  A total of " + str(longSeqNum) + " (" + str(longSeqPerc) + "%) are " +
      str(maxseqB) + "bp long.\n" +
      "||  Writing sequences with  "  + str(maxseqB) + "bp to: " + data_n + "_filtered\n" +
      "||  Writing sequences under " + str(maxseqB) + "bp to: " + data_n + "_removed\n||")

# Tests


# Printing entire log to txt?

# print("||  Done! - " + ) # Print how many sequences and % will remain
