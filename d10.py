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

ex5 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

ex6 = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""

ex7 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

ex8 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


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

def sub(a: (int, int), b: (int, int)) -> (int, int):
    return (a[0] - b[0], a[1] - b[1])

def cross(a: (int, int), b: (int, int)) -> int:
    return a[0] * b[1] - a[1] * b[0]


def at(m, l):
    return m[l[0]][l[1]]


def f1(m: list[str]) -> None:
    dists = [[0 for x in range(len(m[0]))] for y in range(len(m))]

    def is_v(a):
        return a[0] >= 0 and a[0] < len(m) and a[1] >= 0 and a[1] < len(m[0])

    start = finds(m)
    q = deque()
    visited = {}

    def maybe_add(l, dir):
        match dir:
            case "R":
                mov = RMOV
            case "L":
                mov = LMOV
            case "D":
                mov = DMOV
            case "U":
                mov = UMOV
            case "O":
                mov = (0, 0)
        l0 = l[-1]
        new_l = add(l0, mov)
        if is_v(new_l):
            if (
                (dir == "L" and at(m, new_l) in "L-F")
                or (dir == "R" and at(m, new_l) in "7-J")
                or (dir == "U" and at(m, new_l) in "7|F")
                or (dir == "D" and at(m, new_l) in "J|L")
                or dir == "O"
            ):
                if dir == "O":
                    l = []
                q.append((l, new_l, dir))

    maybe_add([start], "O")
    dists[start[0]][start[1]] = 0
    while q:
        old_l, l, dir = q.popleft()
        combined_l = old_l + [l]
        if l in visited:
            dist = dists[l[0]][l[1]]
            old_l2 = visited[l]
            path = old_l + [l] + list(reversed(old_l2))
            print("found", l, "from", len(path), dist)
            return path, dist
        visited[l] = old_l
        ch = m[l[0]][l[1]]
        if dir != "O":
            old_l0 = old_l[-1]
            newdist = dists[old_l0[0]][old_l0[1]] + 1
            dists[l[0]][l[1]] = newdist
            # print(l, newdist)
        # print("====")
        # print("\n".join("".join((str(y) + ",") for y in x) for x in dists))
        if ch == "S":
            maybe_add(combined_l, "L")
            maybe_add(combined_l, "R")
            maybe_add(combined_l, "U")
            maybe_add(combined_l, "D")
        elif (
            (ch == "J" and dir == "R")
            or (ch == "|" and dir == "U")
            or (ch == "L" and dir == "L")
        ):
            # Up
            maybe_add(combined_l, "U")
        elif (
            (ch == "-" and dir == "R")
            or (ch == "L" and dir == "D")
            or (ch == "F" and dir == "U")
        ):
            # Right
            maybe_add(combined_l, "R")
        elif (
            (ch == "|" and dir == "D")
            or (ch == "7" and dir == "R")
            or (ch == "F" and dir == "L")
        ):
            # Down
            maybe_add(combined_l, "D")
        elif (
            (ch == "-" and dir == "L")
            or (ch == "7" and dir == "U")
            or (ch == "J" and dir == "D")
        ):
            # Left
            maybe_add(combined_l, "L")

def rotdir(a: (int, int), dir: str) -> (int, int):
    if dir == "L":
        return (a[1] * 1, a[0] * -1)
    else:
        return (a[1] * -1, a[0] * 1)


def f2(inp):
    pipes, _ = f1(inp)
    M = len(inp)
    N = len(inp[0])
    spipes = set(pipes)
    def ffill(loc: (int, int)):
        if loc in spipes:
            return set()
        to_visit = deque()
        to_visit.append(loc)
        visited = set()
        while to_visit:
            l = to_visit.popleft()
            if l in visited:
                continue
            visited.add(l)
            for mov in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                newp = add(mov, l)
                if newp[0] >= 0 and newp[0] < M and newp[1] >= 0 and newp[1] < N:
                    if newp not in spipes:
                        to_visit.append(newp)
        return visited

    dirs = []
    for i in range(len(pipes) - 1):
        dirs.append(sub(pipes[i + 1], pipes[i]))
    crosses = 0
    for i in range(len(dirs) - 1):
        crosses += cross(dirs[i], dirs[i + 1])
    print(crosses)
    if crosses > 0:
        handed = "R"
    else:
        handed = "L"
    insides = set()
    for i in range(len(dirs)):
        rdir = rotdir(dirs[i], handed)
        loc = add(pipes[i], rdir)
        u = ffill(loc)
        insides.update(u)
        loc = add(pipes[i + 1], rdir)
        u = ffill(loc)
        insides.update(u)
    # print(insides)
    
    for ai, a in enumerate(inp):
        for b in range(len(a)):
            if (ai, b) in spipes:
                print(inp[ai][b], end="")
            elif (ai, b) in insides:
                print("I", end="")
            else:
                print(".", end="")
        print("")
    return len(insides)
            

d10 = open("d10.txt").read()

datas = [ex1, ex2, ex3, ex4, d10]
# [print(f1(x.splitlines())[1]) for x in datas]
print("p2")
[print("ans=", f2(x.splitlines())) for x in [ex5, ex6, ex7, ex8, d10]]

