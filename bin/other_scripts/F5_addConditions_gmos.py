#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:17:56 2020

@author: Fred Jaya
"""

import re
import csv 

def check_line(line):
    if re.fullmatch("\n", line):
        return("newline")
    elif re.match("-------------", line):
        return("query_name")
    else:
        return("subject_mosaic")

r_query_name = re.compile("(?<=\)\s).*(?=\s-)")
header = ["query_name", "query_start", "query_end", "significance", 
          "query_end_dupe", "score", "E-value", "short_subject_name", 
          "full_subject_name", "subject_start", "subject_end", "subject_strand"]
    
with open("/Users/13444841/Dropbox/Masters/02_working/2002_gmos_conditions/"
          "hcv_emp037_gmos_out.txt", 'r') as gmos_in:
    
    with open("/Users/13444841/Dropbox/Masters/02_working/2002_gmos_conditions/"
              "gmos_out.csv", 'w') as csv_out:
    
        writer = csv.writer(csv_out)
        writer.writerow(header)
       
        q = []
        
        for line in gmos_in:
            if check_line(line) == "query_name":
                q = re.findall(r_query_name, line)
            if check_line(line) == "subject_mosaic":
                sm = line.split()
                writer.writerow(q + sm)
            else:
                None
    