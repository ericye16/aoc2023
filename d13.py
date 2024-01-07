ex1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split(
    "\n\n"
)

d13 = open("d13.input").read().split("\n\n")


def mirroredrow(r: int, m: list[str]) -> int:
    def roweq(ra, rb):
        l = 0
        for c in range(len(m[0])):
            if m[ra][c] != m[rb][c]:
                l += 1
        return l

    ll = 0
    for ri in range(min(r, len(m) - r)):
        ll += roweq(r - ri - 1, r + ri)
    return ll


def mirroredcol(c: int, m: list[str]) -> int:
    def coleq(cidxa, cidxb):
        l = 0
        for i in range(len(m)):
            if m[i][cidxa] != m[i][cidxb]:
                l += 1
        return l

    ll = 0
    for ci in range(min(c, len(m[0]) - c)):
        ll += coleq(c - ci - 1, c + ci)
    return ll


def p1(inp: str, n=0) -> (int, int):
    inp = inp.splitlines()
    for r in range(1, len(inp)):
        if mirroredrow(r, inp) == n:
            return r, 0
    for c in range(1, len(inp[0])):
        if mirroredcol(c, inp) == n:
            return 0, c


def p(i):
    pp = [p1(x) for x in i]
    # print(pp)
    print(sum([a * 100 + b for (a, b) in pp]))

    pp = [p1(x, 1) for x in i]
    # print(pp)
    print(sum([a * 100 + b for (a, b) in pp]))


if __name__ == "__main__":
    p(ex1)
    p(d13)
