import sys

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

prev = None
ix = 1
running = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if prev is None:
        prev = eval(line)
    else:
        cur = eval(line)
        c = cmpr(prev, cur)
        print(f'ix {ix} left {prev} right {cur} res {c}')
        if c is True:
            running += ix
        ix += 1
        prev = None

print('sum:', running)
