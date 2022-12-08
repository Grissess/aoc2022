import sys

hm = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    hm.append(list(map(int, line)))

height, width = len(hm), len(hm[0])
vm = [[False for _ in range(width)] for _ in range(height)]

def raycast(x, y, dx, dy, hwm=-1):
    vm[y][x] = vm[y][x] or (hm[y][x] > hwm)
    hwm = max(hwm, hm[y][x])
    nx, ny = x + dx, y + dy
    if (not (0 <= nx < width)) or (not (0 <= ny < height)):
        return
    raycast(nx, ny, dx, dy, hwm)

for x in range(width):
    raycast(x, 0, 0, 1)
    raycast(x, height - 1, 0, -1)
for y in range(height):
    raycast(0, y, 1, 0)
    raycast(width - 1, y, -1, 0)

VIS, NVIS = '\x1b[1;31m', '\x1b[34m'
for y, row in enumerate(hm):
    for x, ht in enumerate(row):
        v = vm[y][x]
        print(VIS if v else NVIS, ht, sep='', end='')
    print()

print('vis:', sum(sum(1 if v else 0 for v in r) for r in vm))
