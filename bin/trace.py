#!/usr/bin/env python3

import pandas as pd
import re
import numpy as np

def nf_hours(t):
    t = str(t)
    total_hours = 0
    if re.findall('ms', t) == ['ms']:
            total_hours += 1/60 # minute
    else:
        if re.findall('d', t) == ['d']:
            days = re.findall('\d+(?=d)', t)
            total_hours += int(days[0]) * 24
        if re.findall('h', t) == ['h']:
            hours = re.findall('\d+(?=h)', t)
            total_hours += int(hours[0])
        if re.findall('m', t) == ['m']:
            mins = re.findall('\d+(?=m)', t)
            total_hours += int(mins[0]) / 60
        if re.findall('s', t) == ['s']:
            total_hours += 1/60 # minute
    return(total_hours)

# Check for unique time combos
def nf_unique_times(df_col):
    rt = df['realtime']
    rt_unique = []
    for i in rt:
        i = str(i)
        i = re.sub('[^a-z]', '', i)
        rt_unique.append(i)
    rt_unique = np.unique(rt_unique)
    print(rt_unique)

####
####

df = pd.read_csv("~/GitHub/rec-bench/out/trace/trace_all.csv")
df = df.drop(columns = ['task_id', 'status', 'exit'])
#drop_rows = df.realtime != '-'
#df = df[drop_rows]

nf_times = []
for row in df['realtime']:
    total_hours = nf_hours(row)
    nf_times.append(total_hours)
df['parsed_hours'] = nf_times
print('Writing /out/trace/nf_times.csv')
df.to_csv('~/GitHub/rec-bench/out/trace/nf_times.csv')
