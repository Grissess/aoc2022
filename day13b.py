import sys
import functools
import operator

DIVIDERS = (
    [[2]],
    [[6]],
)

def cmpr(l, r, lv=0):
    print(f'{" "*lv}cmpr({l},{r})')
    li, ri = isinstance(l, int), isinstance(r, int)
    if li and ri:
        if l < r:
            return True
        if l > r:
            return False
    elif not (li or ri):
        for lx, rx in zip(l, r):
            c = cmpr(lx, rx, lv+1)
            if c is not None:
                return c
        if len(l) < len(r):
            return True
        if len(l) > len(r):
            return False
    else:
        lp, ip, sw = (l, r, False) if ri else (r, l, True)
        return cmpr([ip], lp, lv+1) if sw else cmpr(lp, [ip], lv+1)

@functools.total_ordering
class Cpr:
    def __init__(self, v):
        self.v = v

    def __eq__(self, o):
        return self.v == o.v

    def __lt__(self, r):
        return cmpr(self.v, r.v) is True

items = [Cpr(i) for i in DIVIDERS]
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    items.append(Cpr(eval(line)))

items.sort()

print('sort:')
dp = []
for ix, i in enumerate(items):
    print(i.v)
    if i.v in DIVIDERS:
        dp.append(ix+1)

print('key:', functools.reduce(operator.mul, dp, 1))
