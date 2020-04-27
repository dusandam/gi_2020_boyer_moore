import argparse
import subprocess
import sys

if sys.version_info[:2] < (3, 0):
    code=subprocess.call(['python3'] + sys.argv)
    raise SystemExit(code)

import matplotlib.pyplot as plt
from heuristics.good_suffix import GoodSuffix
from heuristics.bad_character import BadCharacter
from heuristics.horspool_sunday import HorspoolSunday
from heuristics.horspool_sunday_2 import HorspoolSunday2
import boyer_moore as bm
import timeit
import tracemalloc


def get_text(text):
    return "".join(sorted(set(text)))


def get_heuristics_name(heurisitcs):
    ret=[heuristic.get_name() for heuristic in heurisitcs]
    ret=' and '.join(ret)
    return ret


heuristics=[]

abbreviations=["1 + 2", "1", "2", "BC + GS"]

colors=["r", "b", "g", "y"]
index=0
sorted_files=[]
positions=[]

parser=argparse.ArgumentParser()
parameters=parser.add_argument_group('required arguments')

parameters.add_argument("-hh", "--heuristic", type=int, required=True, metavar='', nargs='+', choices=range(1, 4))
# chosing heuristics option
parameters.add_argument("-f", "--file", type=argparse.FileType('r', encoding='UTF-8'), required=True, metavar='')
# file path
parameters.add_argument("-p", "--pattern", type=str, metavar='', required=True)
# pattern

args=parser.parse_args()

heur_dict={
    1: [BadCharacter()],
    2: [GoodSuffix()],
    3: [HorspoolSunday()],
    4: [HorspoolSunday2()]
}

if __name__ == '__main__':
    args.file.seek(0)
    for i in args.heuristic:
        heuristics.append(heur_dict.get(i))

    memory_in_bytes_all=[]
    time_in_s_all=[]
    positions_all=[]
    test_names=[]
    patterns=[]
    plt.rcParams['xtick.labelsize']=7
    f1=plt.figure(1)

    for algorithm in heuristics:
        time_in_s=[]
        memory_in_bytes=[]
        bm.set_heuristics(algorithm)

        text=args.file.read()
        text=[line.rstrip("\n\r") for line in text]
        text=''.join(text[1:])

        pattern=args.pattern
        test_name="File: " + str(args.file) + "\nPattern: " + pattern
        test_names.append(test_name)

        tracemalloc.start()
        bm.preprocess(pattern, get_text(text))
        mem=round(tracemalloc.get_tracemalloc_memory(), 2)
        memory_in_bytes.append(mem)
        tracemalloc.stop()
        time=min(timeit.repeat('boyer_moore(text)', number=1, repeat=5,
                               setup='from boyer_moore import boyer_moore; text=\"' + text + "\""))
        time_in_s.append(round(time, 2))

        print(get_heuristics_name(algorithm) + " finished in " + str(round(time, 2)) + " s and used " + str(mem) + "B")

    args.file.close()
