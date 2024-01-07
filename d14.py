from tqdm import tqdm


ex1 = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".splitlines()

d14 = open("d14.input").read().splitlines()


def shiftN(m: list[list[str]]) -> bool:
    moved = False
    for ridx in range(1, len(m)):
        for cidx in range(len(m[0])):
            if m[ridx - 1][cidx] == "." and m[ridx][cidx] == "O":
                m[ridx - 1][cidx] = "O"
                m[ridx][cidx] = "."
                moved = True
    return moved


def shiftE(m: list[list[str]]) -> bool:
    moved = False
    for cidx in range(len(m[0]) - 1):
        for ridx in reversed(range(len(m))):
            if m[ridx][cidx + 1] == "." and m[ridx][cidx] == "O":
                m[ridx][cidx + 1] = "O"
                m[ridx][cidx] = "."
                moved = True
    return moved


def shiftS(m: list[list[str]]) -> bool:
    moved = False
    for ridx in reversed(range(len(m) - 1)):
        for cidx in range(len(m[0])):
            if m[ridx + 1][cidx] == "." and m[ridx][cidx] == "O":
                m[ridx + 1][cidx] = "O"
                m[ridx][cidx] = "."
                moved = True
    return moved


def shiftW(m: list[list[str]]) -> bool:
    moved = False
    for cidx in range(1, len(m[0])):
        for ridx in range(len(m)):
            if m[ridx][cidx - 1] == "." and m[ridx][cidx] == "O":
                m[ridx][cidx - 1] = "O"
                m[ridx][cidx] = "."
                moved = True
    return moved


def shift(m: tuple[str], dir="N") -> list[list[str]]:
    m2 = [[x for x in l] for l in m]
    if dir == "N":
        shift_f = shiftN
    elif dir == "E":
        shift_f = shiftE
    elif dir == "S":
        shift_f = shiftS
    else:
        shift_f = shiftW
    while shift_f(m2):
        pass
    return m2


def score(m):
    s = 0
    R = len(m)
    for ridx, l in enumerate(m):
        for c in l:
            if c == "O":
                s += R - ridx
        print("".join(l))
    return s


def p(m: list[str]) -> int:
    m2: tuple[str] = (l for l in m)
    m3 = shift(m2)
    return score(m3)


def p2(m: list[str]) -> int:
    # N = 3
    N = 1000000000
    h = {}
    n = 0
    dirs = ["N", "W", "S", "E"]
    jumped = False
    with tqdm(total=N) as pbar:
        while n < N:
            m2: tuple[str] = tuple("".join(l) for l in m)
            if not jumped and m2 in h:
                gap = n - h[m2]
                jump = (N - n) // gap * gap
                n += jump
                pbar.update(jump)
                jumped = True
            h[m2] = n
            for dir in dirs:
                m2: tuple[str] = tuple("".join(l) for l in m)
                m = shift(m2, dir)
            # for l in m:
            #     print("".join(l))
            # print()
            n += 1
            pbar.update(1)

    return score(m)


if __name__ == "__main__":
    # print(p2(ex1))
    print(p2(d14))
