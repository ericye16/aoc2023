import sys
from typing import List
from collections import defaultdict


class Game:
  pass

def parse_lines(lines: List[str]) -> List[Game]:
  v = []
  for line in lines:
    game_part, grabs_part = line.split(":")
    game = Game()
    game.id = int(game_part.split(" ")[1])
    grabs = grabs_part.split(";")
    game.grabs = []
    for grab in grabs:
      color_grabs = grab.split(",")
      d = defaultdict(int)
      for color_grab in color_grabs:
        number, color = color_grab.strip().split(" ")
        number = int(number.strip())
        d[color] = number
      game.grabs.append(d)
    v.append(game)
  return v

def p1(lines: List[str]) -> int: 
  games = parse_lines(lines)
  s = 0
  for game in games:
    possible = True
    for grab in game.grabs:
      if grab["red"] > 12 or grab["green"] > 13 or grab["blue"] > 14:
        possible = False
    if possible:
      s += game.id
  return s

def p2(lines: List[str]) -> int:
  games = parse_lines(lines)
  s = 0
  for game in games:
    d = defaultdict(int)
    for grab in game.grabs:
      for color, number in grab.items():
        if number > d[color]:
          d[color] = number
    mul = 1
    for color in ["red", "green", "blue"]:
      mul *= d[color]
    s += mul
  return s


if __name__ == "__main__":
  filename = sys.argv[1]
  lines = open(filename).readlines()

  print(p1(lines))
  print(p2(lines))