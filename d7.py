import sys
from collections import defaultdict
from functools import reduce, cmp_to_key  # only in Python 3
from math import sqrt, floor, ceil


ex = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

order = "AKQJT98765432"

K5 = 6
K4 = 5
FH = 4
K3 = 3
K22 = 2
K2 = 1
K1 = 0


def parse_card(hand):
    cards = defaultdict(int)
    for card in hand:
        cards[card] += 1
    if any(v == 5 for v in cards.values()):
        return K5
    if any(v == 4 for v in cards.values()):
        return K4
    if any(v == 3 for v in cards.values()) and any(v == 2 for v in cards.values()):
        return FH
    if any(v == 3 for v in cards.values()):
        return K3
    if list(cards.values()).count(2) == 2:
        return K22
    if any(v == 2 for v in cards.values()):
        return K2
    return K1

def key(h1):
    return str(parse_card(h1)) + h1

def comp(h1, h2):
    h1 = h1[0]
    h2 = h2[0]
    p1 = parse_card(h1)
    p2 = parse_card(h2)
    if p1 > p2:
        return 1
    elif p2 > p1:
        return -1
    for ch1, ch2 in zip(h1, h2):
        idx1 = order.find(ch1)
        idx2 = order.find(ch2)
        if idx1 < idx2:
            return 1
        elif idx2 < idx1:
            return -1
    return 0



def main():
    # hands = ex.splitlines()
    hands = open("d7.txt").read().splitlines()
    cards = []
    for hand in hands:
        card, bid = hand.split()
        cards.append((card, bid))
    cards_sorted = sorted(cards, key=cmp_to_key(comp))
    p = 0
    for r, (_, bid) in enumerate(cards_sorted):
        p += (r + 1) *int( bid)
    print(p)


if __name__ == "__main__":
    main()
