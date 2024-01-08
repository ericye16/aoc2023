from collections import defaultdict

ex1 = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")

d15 = "".join(open("d15.input").read().splitlines()).split(",")


def h(x):
    cur_val = 0
    for i in x:
        asci = ord(i)
        cur_val += asci
        cur_val *= 17
        cur_val %= 256
    return cur_val


print(h("HASH"))


def p1(inp):
    l = []
    for j in inp:
        l.append(h(j))
    return sum(l)


def p2(inp: list[str]):
    buckets = defaultdict(list)
    for step in inp:
        print(step)
        if "=" in step:
            label, focl = step.split("=")
            focl = int(focl)
            bucket = h(label)
            l = buckets[bucket]
            for li, ll in enumerate(l):
                if ll[0] == label:
                    l[li] = (label, focl)
                    break
            else:
                l.append((label, focl))
        elif "-" in step:
            label = step.removesuffix("-")
            bucket = h(label)
            l = buckets[bucket]
            for li, ll in enumerate(l):
                if ll[0] == label:
                    del l[li]
                    break
        else:
            assert False
        print(buckets)
    s = 0
    for bucket, bucketitems in buckets.items():
        for idx, (_, focl) in enumerate(bucketitems):
            s += (bucket + 1) * (idx + 1) * focl
    return s


print(p2(ex1))
print(p2(d15))
