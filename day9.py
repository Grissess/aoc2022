import sys

signum = lambda x: 0 if x == 0 else 1 if x > 0 else -1

def linf(a, b):
    ax, ay = a
    bx, by = b
    return max(abs(ax - bx), abs(ay - by))

hp = (0, 0)
tp = (0, 0)
vm = {(0, 0)}

def domove(dx, dy):
    global hp, tp
    hx, hy = hp
    hp = (hx + dx, hy + dy)
    if linf(hp, tp) > 1:
        nx, ny = hp
        tx, ty = tp
        cx, cy = nx - tx, ny - ty
        sx, sy = signum(cx), signum(cy)
        tp = (tx + sx, ty + sy)

DMAP = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    dr, _, amt = line.partition(' ')
    dx, dy = DMAP[dr]
    for _ in range(int(amt)):
        domove(dx, dy)
        vm.add(tp)

xs, ys = [p[0] for p in vm], [p[1] for p in vm]
nx, mx, ny, my = min(xs), max(xs), min(ys), max(ys)

for y in range(my, ny - 1, -1):
    for x in range(nx, mx + 1):
        print('#' if (x, y) in vm else '.', end='')
    print()

print('len:', len(vm))
