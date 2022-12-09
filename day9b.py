import sys

signum = lambda x: 0 if x == 0 else 1 if x > 0 else -1

def linf(a, b):
    ax, ay = a
    bx, by = b
    return max(abs(ax - bx), abs(ay - by))

knots = [(0, 0) for _ in range(10)]
vm = {(0, 0)}

def fixup():
    for ix in range(len(knots) - 1):
        hp, tp = knots[ix], knots[ix+1]
        if linf(hp, tp) > 1:
            nx, ny = hp
            tx, ty = tp
            cx, cy = nx - tx, ny - ty
            sx, sy = signum(cx), signum(cy)
            knots[ix+1] = (tx + sx, ty + sy)

def domove(dx, dy):
    hx, hy = knots[0]
    knots[0] = (hx + dx, hy + dy)
    fixup()

DMAP = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    dr, _, amt = line.partition(' ')
    dx, dy = DMAP[dr]
    for _ in range(int(amt)):
        domove(dx, dy)
        vm.add(knots[-1])

xs, ys = [p[0] for p in vm], [p[1] for p in vm]
nx, mx, ny, my = min(xs), max(xs), min(ys), max(ys)

for y in range(my, ny - 1, -1):
    for x in range(nx, mx + 1):
        print('#' if (x, y) in vm else '.', end='')
    print()

print('len:', len(vm))
