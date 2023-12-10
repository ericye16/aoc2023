import sys
from collections import defaultdict
from functools import reduce, cmp_to_key  # only in Python 3
from math import sqrt, floor, ceil, lcm
import re


ex = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

ex2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

ex3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

def f(lines):
    steps = lines[0]

    mapp = lines[2:]
    mapd = {}
    for map0 in mapp:
        print(map0)
        m = re.match(r"(\w+) = \((\w+), (\w+)\)", map0)
        r0 = m.group(1)
        l = m.group(2)
        r = m.group(3)
        mapd[r0] = (l, r)
    steps0 = 0
    curr = "AAA"
    while curr != "ZZZ":
        this_step = steps[steps0 % len(steps)]
        curr = mapd[curr][0 if this_step == "L" else 1]
        steps0 += 1
    print(steps0)

def f2(lines):
    steps = lines[0]

    mapp = lines[2:]
    mapd = {}
    for map0 in mapp:
        print(map0)
        m = re.match(r"(\w+) = \((\w+), (\w+)\)", map0)
        r0 = m.group(1)
        l = m.group(2)
        r = m.group(3)
        mapd[r0] = (l, r)
    currs = []
    for curr in mapd:
        if curr[-1] == "A":
            currs.append(curr)
    stepsv = []
    for cur0 in currs:
        steps0 = 0
        while cur0[-1] != "Z":
            this_step = steps[steps0 % len(steps)]
            cur0 = mapd[cur0][0 if this_step == "L" else 1]
            steps0 += 1
        stepsv.append(steps0)
        print(steps0)
    print(stepsv)
    print(lcm(*stepsv))

def main():
  f(ex.splitlines())
  f(ex2.splitlines())
  f(open("d8.input").read().splitlines())
  f2(ex3.splitlines())
  f2(open("d8.input").read().splitlines())



if __name__ == "__main__":
    main()
