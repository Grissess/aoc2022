import sys

hm = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    hm.append(list(map(int, line)))

height, width = len(hm), len(hm[0])
sc = [[None for _ in range(width)] for _ in range(height)]

def raycast(x, y, dx, dy, hwm, iters=0):
    nx, ny = x + dx, y + dy
    if (not (0 <= nx < width)) or (not (0 <= ny < height)):
        return iters
    if hm[ny][nx] >= hwm:
        return iters + 1
    return raycast(nx, ny, dx, dy, hwm, iters + 1)

for x in range(width):
    for y in range(height):
        h = hm[y][x]
        a = raycast(x, y, 1, 0, h)
        b = raycast(x, y, -1, 0, h)
        c = raycast(x, y, 0, 1, h)
        d = raycast(x, y, 0, -1, h)
        print(f'{x},{y} ({h}) -> {a}, {b}, {c}, {d}')
        sc[y][x] = a*b*c*d

for y, row in enumerate(hm):
    for x, ht in enumerate(row):
        s = sc[y][x]
        print(f'{ht}={s:02d}', sep='', end='')
    print()

print('max:', max(max(row) for row in sc))
