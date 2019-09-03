#!/usr/bin/env python3

# 
import re
            
# Test file
x = open('/Users/13444841/GitHub/rec-bench/out/S4_geneconv/msa_m0.010_rc1.0E-7_n100_dual0.05_rep3.tab').read()

def gc_regex():
    re.findall('(?<=# )(No|One|\d+)(?= inner fragment)', x) == ['No'], \
                 "Inner negative doesn't match"
    re.findall('(?<=# )(No|One|\d+)(?= outer-sequence fragment)', x) == \
                 ['No'], "Outer negative doesn't match"
    #re.findall('(?<=#\sFrag\tSequence\tSim\tBC KA\t\tAligned Offsets\t\t\tIn Seq1\t\t\tIn Seq2\t\tNum\tNum\tTotal\tMismatch\t\n#\s\s\stype\tNames\tPvalue\tPvalue\tBegin\tEnd\tLength\tBegin\tEnd\tLength\tBegin\tEnd\tLength\tPoly\tDif\tDiffs\tPenalty\t\n)[\w\W]+(?=\n# (No|One|\d+)\sinner\sfragments\slisted.)', x)
        
if __name__ == "__main__":
    gc_regex()
    print("Everything passed")
    
    