import re
import sys

def l1(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax-bx) + abs(ay-by)

def all_l1(a, d):
    x, y = a
    xmn, xmx, ymn, ymx = x - d, x + d, y - d, y + d
    for nx in range(xmn, xmx + 1):
        for ny in range(ymn, ymx + 1):
            if l1(a, (nx, ny)) <= d:
                yield nx, ny

PARSE = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

sensors = {}
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    mo = PARSE.match(line)
    sx, sy, bx, by = mo.group(1, 2, 3, 4)
    s = (int(sx), int(sy))
    b = (int(bx), int(by))
    sensors[s] = b

beacons = set(sensors.values())

xs = set(i[0] for i in sensors.keys()) | set(i[0] for i in sensors.values())
ys = set(i[1] for i in sensors.keys()) | set(i[1] for i in sensors.values())
xmn, xmx, ymn, ymx = min(xs), max(xs), min(ys), max(ys)
dx, dy = xmx - xmn + 1, ymx - ymn + 1
print(f'bounds {xmn}-{xmx}, {ymn}-{ymx}, size {dx}, {dy}')

CRIT_Y = 10
counter = 0
for x in range(xmn, xmx + 1):
    p = (x, CRIT_Y)
    if x % 10000 == 0:
        print('test', p, counter)
    if p in beacons:
        continue
    for s, b in sensors.items():
        ds = l1(p, s)
        db = l1(s, b)
        if ds <= db:
            #print(f'passed: sens {s} beac {b} dist {db} (to us: {ds})')
            counter += 1
            break

print('positions:', counter)
