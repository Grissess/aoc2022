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

def isct(s, d, y):
    sx, sy = s
    dy = abs(y-sy)
    if dy > d:
        return None
    df = d - dy
    return (sx - df, y), (sx + df, y)

CRIT_Y = int(sys.argv[1])
ivs = []
for s, b in sensors.items():
    i = isct(s, l1(s, b), CRIT_Y)
    print(f'crossovers for {s}: {b}: {i}')
    if i is not None:
        l, r = i
        ivs.append((l[0], r[0]))

print('pre-un:', ivs)

def unite(a, b):
    na, nb, ma, mb = min(a), min(b), max(a), max(b)
    al = a+b
    n, m = min(al), max(al)
    if ma >= nb or mb >= na:
        return (n, m), None
    return a, b

i = 0
while i < len(ivs) - 1:
    a, b = unite(ivs[i], ivs[i+1])
    if b is None:
        ivs[i] = a
        del ivs[i+1]
    else:
        i += 1

print('intervals:', ivs)

def cut(a, p):
    l, h = a
    if l == p:
        return (l+1, h), None
    if h == p:
        return (l, h-1), None
    if l < p < h:
        return (l, p-1), (p+1, h)
    return (l, h), None

for b in beacons:
    if b[1] == CRIT_Y:
        print('cut:', b)
        nivs = []
        for iv in ivs:
            a, i = cut(iv, b[0])
            nivs.append(a)
            if i is not None:
                nivs.append(i)
        ivs = nivs

print('intervals:', ivs)

print('positions:', sum(h - l + 1 for l, h in ivs))
