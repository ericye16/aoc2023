ex1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()

d11 = open("d11.input").read().splitlines()

def p1(inp: list[str], nt: int) -> int:
  gals = []
  lines_with_gal = set()
  cols_with_gal = set()
  ml = -1
  mc = -1
  for li, l in enumerate(inp):
    for ci, c in enumerate(l):
      if c == "#":
        lines_with_gal.add(li)
        cols_with_gal.add(ci)
        gals.append([li, ci])
        if ci > mc:
          mc = ci
        ml = li
  # print(gals)
  def expand(nt: int):
    el = []
    for l in range(ml):
      if l not in lines_with_gal:
        el.append(l)
    for gal in gals:
      numl = sum([1 if x < gal[0] else 0 for x in el])
      gal[0] += numl * (nt - 1)
    ec = []
    for c in range(mc):
      if c not in cols_with_gal:
        ec.append(c)
    for gal in gals:
      numc = sum([1 if x < gal[1] else 0 for x in ec])
      gal[1] += numc * (nt - 1)
  
  expand(nt)
  dists = 0
  # print(gals)
  for gidx, gal in enumerate(gals):
    for gidx2 in range(gidx + 1, len(gals)):
      g2 = gals[gidx2]
      dist = abs(gal[0] - g2[0]) + abs(gal[1] - g2[1])
      dists += dist
  return dists

print(p1(ex1, 2))
print(p1(d11, 2))

print("---")
print(p1(ex1, 10))
print(p1(ex1, 100))

print("---")
print(p1(d11, 1000000))
  
      