import subprocess
import sys

if sys.version_info[:2] < (3, 0):
    code=subprocess.call(['python3'] + sys.argv)
    raise SystemExit(code)

import matplotlib.pyplot as plt
import pandas as pd
import os

performance_directory="./performance"

dirpath=os.path.abspath(performance_directory)
all_files=(os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)

all_patterns=[]
colors = ["b", "g", "c", "m"]

def get_abbreviation(text):
    if text == 'Horspool Sunday and Horspool Sunday 2':
        return 'HS + HS2'
    else:
        if text == 'Horspool Sunday':
            return 'HS'
        else:
            if text == 'Horspool Sunday 2':
                return 'HS2'
            else:
                if text == 'Good suffix and Bad character':
                    return 'GS + BC'
    return ''

rows=[]
time_all=[]
mem_all=[]

for filepath in all_files:
    file=pd.read_csv(filepath)
    df=pd.DataFrame(file)
    patterns=df['pattern']
    file_name=df['file name']
    x=df['algorithm']
    x_value = []
    i=0
    for alg in x:
        x_value.append(get_abbreviation(alg))
        i=i+1
    time=df['time']
    memory=df['memory']
    test_name="File name: " + file_name[0] + ": " + patterns[0]
    rows.append(test_name)

    time_all.append(time[:])
    mem_all.append(memory[:])

plt.title("Time table")

time_table = plt.table(cellText=time_all,
                       rowLabels=rows,
                       colColours=colors,
                       colWidths=[0.04 for x in time_all],
                       colLabels=x_value,
                       loc='center'
                       )
time_table.auto_set_font_size(False)
time_table.set_fontsize(8)
time_table.scale(2, 2)  # may help

fig, ax=plt.subplots()
plt.title("Memory table")
memo_table = plt.table(cellText=mem_all,
                       rowLabels=rows,
                       colColours=colors,
                       colWidths=[0.04 for x in mem_all],
                       colLabels=x_value,
                       loc='center'
                       )
memo_table.auto_set_font_size(False)
memo_table.set_fontsize(8)
memo_table.scale(2, 2)  # may help

plt.show()

