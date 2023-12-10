import sys
from collections import defaultdict
from functools import reduce, cmp_to_key  # only in Python 3
from math import sqrt, floor, ceil, lcm
import re

ex1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

def diff(seq):
    d = []
    for i in range(len(seq) - 1):
        d.append(seq[i + 1] - seq[i])
    return d


def findnext(seq, rev = False):
    if rev:
        seq = list(reversed(seq))
    difflevels = [seq]
    all_zeros = False
    while not all_zeros:
        dd = diff(difflevels[-1])
        difflevels.append(dd)
        if all([x == 0 for x in dd]):
            all_zeros = True
    for level in range(len(difflevels)):
        rlevel = len(difflevels) - level - 1
        if level == 0:
            difflevels[-1].append(0)
        else:
            difflevels[rlevel].append(difflevels[rlevel][-1] + difflevels[rlevel + 1][-1])
    return difflevels[0][-1]

def f1(inp, rev=False):
    seqs = inp.splitlines()
    s = 0
    for seq in seqs:
        s += findnext([int(x) for x in seq.split()], rev=rev)
    print(s)

f1(ex1)
f1(open("d9.input").read())
f1(ex1, rev=True)
f1(open("d9.input").read(), rev=True)
