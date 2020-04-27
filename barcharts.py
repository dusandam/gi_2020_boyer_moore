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

index = 0

for filepath in all_files:
    file=pd.read_csv(filepath)
    df=pd.DataFrame(file)
    print(df)
    patterns=df['pattern']
    file_name=df['file name']

    print(all_patterns)
    x=df['algorithm']
    x_value = []
    i=0
    for alg in x:
        x_value.append(get_abbreviation(alg))
        i=i+1
    time=df['time']
    memory=df['memory']
    test_name="File name: " + file_name[0] + " \nPattern: " + patterns[0]
    index = index + 1
    plt.figure(index)

    plt.bar(x_value[:], time[:], color=colors[:])

    plt.title("Time performance for:" + test_name)
    plt.xlabel('Heuristic')
    plt.ylabel('Time(s)')

    index = index + 1
    plt.figure(index)
    plt.bar(x_value[:], memory[:], color=colors[:])

    plt.title("Memory performance for:" + test_name)
    plt.xlabel('Heuristic')
    plt.ylabel('Memory(B)')

    plt.show()

plt.show()

