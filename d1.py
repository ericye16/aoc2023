import sys
from typing import Optional

def p1(lines):
  s = 0
  for line in lines:
    first_dig = None
    last_dig = None
    for ch in line:
      if ch.isdigit():
        last_dig = int(ch)
        if first_dig is None:
          first_dig = int(ch)
    digs = first_dig * 10 + last_dig
    s += digs
  return s

def p2(lines):
  
  def get_dig(line_slice: str) -> Optional[int]:
    if line_slice[0].isdigit():
      return int(line_slice[0])
    elif line_slice.startswith("one"):
      return 1
    elif line_slice.startswith("two"):
      return 2
    elif line_slice.startswith("three"):
      return 3
    elif line_slice.startswith("four"):
      return 4
    elif line_slice.startswith("five"):
      return 5
    elif line_slice.startswith("six"):
      return 6
    elif line_slice.startswith("seven"):
      return 7
    elif line_slice.startswith("eight"):
      return 8
    elif line_slice.startswith("nine"):
      return 9
    else:
      return None

  s = 0
  for line in lines:
    first_dig = None
    last_dig = None
    for chidx in range(len(line)):
      line_slice = line[chidx:]
      maybe_dig = get_dig(line_slice)
      if maybe_dig is not None:
        last_dig = maybe_dig
        if first_dig is None:
          first_dig = maybe_dig
    digs = first_dig * 10 + last_dig
    s += digs
  return s

if __name__ == "__main__":
  filename = sys.argv[1]
  lines = open(filename).readlines()

  print(p1(lines))
  print(p2(lines))