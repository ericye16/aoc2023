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


def mirroredrow(r: int, m: list[str]) -> bool:
    for ri in range(min(r, len(m) - r)):
        if m[r - ri - 1] != m[r + ri]:
            return False
    return True


def mirroredcol(c: int, m: list[str]) -> bool:
    def coleq(cidxa, cidxb):
        for i in range(len(m)):
            if m[i][cidxa] != m[i][cidxb]:
                return False
        return True

    for ci in range(min(c, len(m[0]) - c)):
        if not coleq(c - ci - 1, c + ci):
            return False
    return True


def p1(inp: str) -> int:
    inp = inp.splitlines()
    for r in range(1, len(inp)):
        if mirroredrow(r, inp):
            return r * 100
    for c in range(1, len(inp[0])):
        if mirroredcol(c, inp):
            return c


def p(i):
    pp = [p1(x) for x in i]
    print(pp)
    print(sum(pp))


if __name__ == "__main__":
    p(ex1)
    p(d13)
