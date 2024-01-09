from dataclasses import dataclass
import copy

ex1 = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""".splitlines()

d16 = open("d16.input").read().splitlines()


@dataclass(unsafe_hash=True)
class Beam:
    dir: str
    loc: (int, int)


def at(m, beam: Beam):
    return m[beam.loc[0]][beam.loc[1]]


def add(a: (int, int), b: (int, int)) -> (int, int):
    return (a[0] + b[0], a[1] + b[1])


def adv(b: Beam) -> Beam:
    if b.dir == "R":
        n = Beam(b.dir, add(b.loc, (0, 1)))
    elif b.dir == "L":
        n = Beam(b.dir, add(b.loc, (0, -1)))
    elif b.dir == "U":
        n = Beam(b.dir, add(b.loc, (-1, 0)))
    elif b.dir == "D":
        n = Beam(b.dir, add(b.loc, (1, 0)))
    return n


def printenergized(m, energized, beamloc):
    for r in range(len(m)):
        for c in range(len(m[0])):
            if beamloc[0] == r and beamloc[1] == c:
                print("*", end="")
            elif (r, c) in energized:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print("====")


def p1(inp):
    beams = [Beam("R", (0, 0))]
    energized = set()
    visited = set()
    while beams:
        beam = beams.pop()
        if (
            beam.loc[0] < 0
            or beam.loc[0] >= len(inp)
            or beam.loc[1] < 0
            or beam.loc[1] >= len(inp[0])
            or beam in visited
        ):
            continue
        # printenergized(inp, energized, beam.loc)
        energized.add(beam.loc)
        visited.add(beam)
        a = at(inp, beam)
        if (
            a == "."
            or ((beam.dir == "L" or beam.dir == "R") and a == "-")
            or ((beam.dir == "U" or beam.dir == "D") and a == "|")
        ):
            newbeam = adv(beam)
            beams.append(newbeam)
        elif a == "/":
            nb = copy.deepcopy(beam)
            if beam.dir == "U":
                nb.dir = "R"
            elif beam.dir == "R":
                nb.dir = "U"
            elif beam.dir == "D":
                nb.dir = "L"
            elif beam.dir == "L":
                nb.dir = "D"
            else:
                assert False
            nb = adv(nb)
            beams.append(nb)
        elif a == "\\":
            nb = copy.deepcopy(beam)
            if beam.dir == "U":
                nb.dir = "L"
            elif beam.dir == "L":
                nb.dir = "U"
            elif beam.dir == "D":
                nb.dir = "R"
            elif beam.dir == "R":
                nb.dir = "D"
            else:
                assert False
            nb = adv(nb)
            beams.append(nb)
        elif a == "|" and (beam.dir == "L" or beam.dir == "R"):
            upb = copy.deepcopy(beam)
            upb.dir = "U"
            upb = adv(upb)
            downb = copy.deepcopy(beam)
            downb.dir = "D"
            downb = adv(downb)
            beams.extend([upb, downb])
        elif a == "-" and (beam.dir == "U" or beam.dir == "D"):
            upb = copy.deepcopy(beam)
            upb.dir = "L"
            upb = adv(upb)
            downb = copy.deepcopy(beam)
            downb.dir = "R"
            downb = adv(downb)
            beams.extend([upb, downb])
        else:
            print(a, beam)
            assert False

    return len(energized)


# print(p1(ex1))
print(p1(d16))
