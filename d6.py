import sys
from collections import defaultdict
from functools import reduce # only in Python 3
from math import sqrt, floor, ceil

def ways_to_win_race(pair):
    time, dist = pair
    v1 = (time + sqrt(time ** 2 - 4 * dist)) / 2
    if v1 % 1 == 0:
        v1 -= 1
    v2 = (time - sqrt(time ** 2 - 4 * dist)) / 2
    if v2 % 1 == 0:
        v2 += 1
    print(v1, v2)
    return floor(v1) - ceil(v2) + 1



def main():
    races = ((7, 9), (15, 40), (30, 200))
    ways_to_win = list( map(ways_to_win_race, races))
    print(list(ways_to_win))
    print(reduce(lambda x, y: x * y, ways_to_win))

    races = ((71530, 940200),)
    ways_to_win = list( map(ways_to_win_race, races))
    print(list(ways_to_win))
    print(reduce(lambda x, y: x * y, ways_to_win))

    races = ((60947882, 475213810151650),)
    ways_to_win = list( map(ways_to_win_race, races))
    print(list(ways_to_win))
    print(reduce(lambda x, y: x * y, ways_to_win))


if __name__ == "__main__":
    main()
