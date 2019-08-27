#!/usr/bin/env python3

import pandas as pd
import re
import numpy as np
import time
import datetime as dt

def nf_timeparse(x):
    nf_time = []
    # Where x is the realtime col
    for row in x:
        row = str(row)
        days = 0
        hours = 0
        mins = 0
        if re.findall('ms', row) == ['ms']:
            mins = 1
        elif re.findall('d', row) == ['d']:
            days = re.findall('\d+(?=d)', row)
            days = int(days[0])
        elif re.findall('h', row) == ['h']:
            hours = re.findall('\d+(?=h)', row)
            hours = int(hours[0])
        elif re.findall('m', row) == ['m']:
            mins = re.findall('\d+(?=m)', row)
            mins = int(mins[0])
        elif re.findall('s', row) == ['s']:
             mins = 1
        temp = dt.timedelta(days = days, hours = hours, minutes = mins)
        print(temp)
        nf_time.append(temp)
        return(nf_time)

df = pd.read_csv("~/GitHub/rec-bench/out/trace/trace_all.csv")
df = df.drop(columns = ['Unnamed: 0', 'task_id', 'status', 'exit'])
drop_rows = df.realtime != '-'
df = df[drop_rows]

nf_time = nf_timeparse(df['realtime'])    

# Check for unique time combos
rt = df['realtime']
rt_unique = []
for i in rt:
    i = str(i)
    i = re.sub('[^a-z]', '', i)
    rt_unique.append(i)
rt_unique = np.unique(rt_unique) 
print(rt_unique)