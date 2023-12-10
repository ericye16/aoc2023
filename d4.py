import sys
from collections import defaultdict


def main():
  filename = sys.argv[1]
  lines = open(filename).readlines()
  s = 0
  for line in lines:
    _, nos = line.split(":")
    winning, in_hand = nos.split("|")
    winning = set(map(int, filter(None, winning.strip().split(" "))))
    in_hand = set(map(int, filter(None, in_hand.strip().split(" "))))
    ints = len(winning.intersection(in_hand))
    if ints:
      s += 2 ** (ints - 1)
  print(s)
  won_cards = defaultdict(int)
  s = 0
  for line_idx, line in enumerate(lines):
    card, nos = line.split(":")
    _, card_idx = card.split()
    card_idx = int(card_idx)
    winning, in_hand = nos.split("|")
    winning = set(map(int, filter(None, winning.strip().split())))
    in_hand = set(map(int, filter(None, in_hand.strip().split())))
    ints = len(winning.intersection(in_hand))
    wons = 1 + won_cards[card_idx]
    s += 1
    for i in range(1, 1 + ints):
      won_cards[card_idx + i] += wons
      s += wons

  print(s)


if __name__ == "__main__":
  main()