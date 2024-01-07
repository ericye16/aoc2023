import copy
from functools import lru_cache
from multiprocessing import Pool
from tqdm.contrib.concurrent import process_map  # or thread_map


ex0 = """#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1""".splitlines()

ex1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()

d12 = open("d12.input").read().splitlines()


@lru_cache
def countn(l: str, r: list[int]) -> int:
    op = False
    lidx = 0
    ridx = 0
    oplen = 0
    while lidx <= len(l):
        # print(lidx, ridx, op, oplen)
        if lidx == len(l) or l[lidx] == ".":
            if op:
                if ridx >= len(r) or r[ridx] != oplen:
                    return 0
                ridx += 1
            op = False
            oplen = 0
        elif l[lidx] == "#":
            op = True
            oplen += 1
        elif l[lidx] == "?":
            if op:
                if ridx >= len(r):
                    return 0
                elif oplen == r[ridx]:
                    a = countn("." + l[lidx + 1:], r[ridx + 1:])
                    b = 0
                elif oplen > r[ridx]:
                    return 0
                else:
                    # oplen < r[ridx]
                    a = 0
                    b = countn("#" + l[lidx + 1:], (r[ridx] - oplen,) + r[ridx + 1:])
            else:
                a = countn("." + l[lidx + 1:], r[ridx:])
                b = countn("#" + l[lidx + 1:], r[ridx:])
            return a + b
        lidx += 1
    if ridx == len(r):
        # print("".join(l))
        return 1
    else:
        return 0


def p(x, mul=1):
    l, r = x.split(" ")
    r = tuple(int(z) for _ in range(mul) for z in r.split(","))
    if mul != 1:
        l2 = (l + "?") * (mul - 1)
    l = l2 + l
    # print(l, r)
    return countn(l, r)


def _f(x):
    return p(x, 5)


def p1(inp):
    # p1_l = [p(x) for x in inp]
    # print(p1_l)
    # print(sum(p1_l))

    ss = process_map(_f, inp, max_workers=9)
    # ss = []
    # for idx, x in enumerate(inp):
    #     ans = p(x, 5)
    #     ss.append(ans)
    #     print(f"{idx + 1}/{len(inp)}: {ans}")
    # p1_l = [p(x, 5) for x in inp]
    # print(p1_l)
    print(sum(ss))


if __name__ == "__main__":
    # p1(ex0[0:1])
    # p1(ex1)
    p1(d12)
