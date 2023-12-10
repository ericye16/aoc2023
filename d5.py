import sys
from collections import defaultdict

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def parse_maps(lines: list[str], start_lines: int) -> (list[(int, int, int)], int):
    i = start_lines + 1
    v = []
    while i < len(lines) and lines[i]:
        dst_start, src_start, rng = [int(x) for x in lines[i].split()]
        v.append((dst_start, src_start, rng))
        i += 1
    return v, i


def p1(lines: list[str]) -> int:
    _, seeds = lines[0].split(":")
    seeds = [int(seed) for seed in seeds.split()]
    i = 1
    mapps = []
    for map_name in [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "fertilizer-to-water map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map:",
        "humidity-to-location map:",
    ]:
        while lines[i] != map_name:
            i += 1
        mapp, i = parse_maps(lines, i)
        mapps.append(mapp)
    m = float("inf")

    def findmap(mapps, seed):
        for dst_start, src_start, rng in mapps:
            if seed >= src_start and seed < src_start + rng:
                soil = dst_start + seed - src_start
                break
        else:
            soil = seed
        return soil

    for seed in seeds:
        for mapp in mapps:
            seed = findmap(mapp, seed)
        if seed < m:
            m = seed
    return m


def p2(lines: list[str]) -> int:
    _, seeds = lines[0].split(":")
    seeds = [int(seed) for seed in seeds.split()]
    seed_pairs = []
    for i in range(len(seeds) // 2):
        seed_pairs.append((seeds[i * 2], seeds[i * 2 + 1]))
    i = 1
    mapps = []
    for map_name in [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "fertilizer-to-water map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map:",
        "humidity-to-location map:",
    ]:
        while lines[i] != map_name:
            i += 1
        mapp, i = parse_maps(lines, i)
        mapps.append(mapp)
    m = float("inf")

    def findmap(mapps, seed_pairs: list[(int, int)]) -> list[(int, int)]:
        v = []
        for dst_start, src_start, rng in mapps:
            new_seed_pairs = []
            while seed_pairs:
                seed_start, seed_length = seed_pairs.pop()
                if src_start <= seed_start and src_start + rng > seed_start:
                    new_start = dst_start + seed_start - src_start
                    new_rng = min(seed_length, rng + src_start - seed_start)
                    v.append((new_start, new_rng))
                    remain_length = seed_length - new_rng
                    if remain_length:
                        new_seed_pairs.append(
                            (seed_start + new_rng, seed_length - new_rng)
                        )
                elif (
                    src_start < seed_start + seed_length
                    and seed_start + seed_length <= src_start + rng
                ):
                    new_start = dst_start
                    new_rng = min(seed_start + seed_length - src_start, rng)
                    v.append((new_start, new_rng))
                    remain_length = seed_length - new_rng
                    if remain_length:
                        new_seed_pairs.append((seed_start, seed_length - new_rng))
                else:
                    new_seed_pairs.append((seed_start, seed_length))
            seed_pairs = new_seed_pairs
        for seed_pair in seed_pairs:
            v.append(seed_pair)
        return v

    for mapp in mapps:
        next_seed_pairs = findmap(mapp, seed_pairs)
        seed_pairs = next_seed_pairs
    for st, _ in seed_pairs:
        if st < m:
            m = st
    return m


def main():
    print(p1(example.splitlines()))
    print(p2(example.splitlines()))
    filename = sys.argv[1]
    lines = open(filename).read().splitlines()
    print(p1(lines))
    print(p2(lines))


if __name__ == "__main__":
    main()
