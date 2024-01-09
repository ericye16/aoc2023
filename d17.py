from collections import deque
from dataclasses import dataclass
import heapq

ex1 = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines()


d17 = open("d17.input").read().splitlines()

R = 0
D = 1
L = 2
U = 3


def adv(dir, r, c, n, cost_map):
    new_cost = 0
    for n0 in range(1, n + 1):
        if dir == R:
            if c + n0 < len(cost_map[0]):
                new_cost += cost_map[r][c + n0]
        elif dir == L:
            if c - n0 >= 0:
                new_cost += cost_map[r][c - n0]
        elif dir == D:
            if r + n0 < len(cost_map):
                new_cost += cost_map[r + n0][c]
        elif dir == U:
            if r - n0 >= 0:
                new_cost += cost_map[r - n0][c]
    if dir == R:
        return (r, c + n, new_cost)
    elif dir == L:
        return (r, c - n, new_cost)
    elif dir == D:
        return (r + n, c, new_cost)
    elif dir == U:
        return (r - n, c, new_cost)
    else:
        assert False


def p1(inp):
    lll = []
    for l in inp:
        ll = []
        for c in l:
            ll.append(int(c))
        lll.append(ll)
    inp = lll
    ROWS = len(inp)
    COLS = len(inp[0])

    def inbound(r, c):
        return r < ROWS and c < COLS and r >= 0 and c >= 0

    dists = []
    for layer in range(4):
        l = []
        for r in range(ROWS):
            ro = []
            for c in range(COLS):
                ro.append(float("inf"))
            l.append(ro)
        dists.append(l)
        # dists[layer][0][0] = 0
    to_visit = []
    heapq.heappush(to_visit, (0, R, 0, 0))
    heapq.heappush(to_visit, (0, D, 0, 0))
    while to_visit:
        n = heapq.heappop(to_visit)
        cost_to_now, layer, r, c = n
        if r == ROWS - 1 and c == COLS - 1:
            return cost_to_now
        if cost_to_now < dists[layer][r][c]:
            # print(layer, r, c, cost_to_now)
            dists[layer][r][c] = cost_to_now
            for i in range(1, 4):
                newr, newc, costs = adv(layer, r, c, i, inp)
                if inbound(newr, newc):
                    if layer == L or layer == R:
                        newls = [U, D]
                    elif layer == U or layer == D:
                        newls = [R, L]
                    else:
                        assert False
                    for l in newls:
                        heapq.heappush(to_visit, (cost_to_now + costs, l, newr, newc))
        else:
            continue


print(p1(ex1))
print(p1(d17))
