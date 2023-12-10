from collections import deque
ex1 = """.....
.S-7.
.|.|.
.L-J.
....."""

ex2 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

ex3 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

ex4 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

def finds(m: list[str]) -> (int, int):
    for i, l in enumerate(m):
        j = l.find("S")
        if j != -1:
            return (i, j)
    return None 

RMOV = (0, +1)
LMOV = (0, -1)
UMOV = (-1, 0)
DMOV = (+1, 0)

def add(a: (int, int), b: (int, int)) -> (int, int):
    return (a[0] + b[0], a[1] + b[1])

def at(m, l):
    return m[l[0]][l[1]]

def f1(m: list[str]) -> None:
    dists = [[0 for x in range(len(m[0]))] for y in range(len(m))]
    def is_v(a):
        return a[0] >= 0 and a[0] < len(m) and a[1] >= 0 and a[1] < len(m[0])
    start = finds(m)
    print(start)
    q = deque()
    visited = set()
    def maybe_add(l, dir):
        match dir:
            case "R": mov = RMOV
            case "L": mov = LMOV
            case "D": mov = DMOV
            case "U": mov = UMOV
            case "O": mov = (0, 0)
        new_l = add(l, mov)
        if is_v(new_l):
            q.append((l, new_l, dir))
    maybe_add(start, "O")
    dists[start[0]][start[1]] = 0
    while q:
        old_l, l, dir = q.popleft()
        if l in visited:
            dist = dists[l[0]][l[1]]
            print("found", l, "from", old_l, dist)
            return dist
        visited.add(l)
        ch = m[l[0]][l[1]]
        if dir != "O":
            newdist = dists[old_l[0]][old_l[1]] + 1
            dists[l[0]][l[1]] = newdist
            # print(l, newdist)
        # print("====")
        # print("\n".join("".join((str(y) + ",") for y in x) for x in dists))
        if ch == "S":
            if at(m, add(l, LMOV)) in "L-F":
                maybe_add(l, "L")
            if at(m, add(l, RMOV)) in "7-J":
                maybe_add(l, "R")
            if at(m, add(l, UMOV)) in "7|F":
                maybe_add(l, "U")
            if at(m, add(l, DMOV)) in "J|L":
                maybe_add(l, "D")
        elif ch == "J" and dir == "R" or ch == "|" and dir == "U" or ch == "L" and dir == "L":
            # Up
            maybe_add(l, "U")
        elif ch == "-" and dir == "R" or ch == "L" and dir == "D" or ch == "F" and dir == "U":
            # Right
            maybe_add(l, "R")
        elif ch == "|" and dir == "D" or ch == "7" and dir == "R" or ch == "F" and dir == "L":
            # Down
            maybe_add(l, "D")
        elif ch == "-" and dir == "L" or ch == "7" and dir == "U" or ch == "J" and dir == "D":
            # Left
            maybe_add(l, "L")

print(f1(ex1.splitlines()))
print(f1(ex2.splitlines()))
print(f1(ex3.splitlines()))
print(f1(ex4.splitlines()))
print(f1(open("d10.txt").read().splitlines()))
