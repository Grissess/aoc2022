import re
import sys

BEACON, SENSOR, CLEAR = object(), object(), object()
def chrf(o):
    if o is None:
        return '.'
    if o is BEACON:
        return 'B'
    if o is SENSOR:
        return 'S'
    if o is CLEAR:
        return '#'
    return '?'

class Grid:
    def __init__(self, w, h, o = (0, 0)):
        self.data = [None for _ in range(w*h)]
        self.width, self.height = w, h
        self.origin = o

    def co(self, x, y):
        ox, oy = self.origin
        ix = (y - oy) * self.width + (x - ox)
        #print(f'co {x},{y} -> {ix} ({len(self.data)})')
        return ix

    def __contains__(self, pr):
        ox, oy = self.origin
        x, y = pr
        lx, ly = x-ox, y-oy
        return 0 <= lx < self.width and 0 <= ly < self.height

    def __getitem__(self, pr):
        (x, y) = pr
        return self.data[self.co(x, y)]

    def __setitem__(self, pr, v):
        (x, y) = pr
        self.data[self.co(x, y)] = v

    def show(self, chrf=chrf):
        ox, oy = self.origin
        for y in range(self.height):
            for x in range(self.width):
                print(f'{chrf(self[x+ox, y+oy])}', end='')
            print()
        print()

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

xs = set(i[0] for i in sensors.keys()) | set(i[0] for i in sensors.values())
ys = set(i[1] for i in sensors.keys()) | set(i[1] for i in sensors.values())
xmn, xmx, ymn, ymx = min(xs), max(xs), min(ys), max(ys)
dx, dy = xmx - xmn + 1, ymx - ymn + 1
grid = Grid(dx, dy, (xmn, ymn))

for s, b in sensors.items():
    grid[s] = SENSOR
    grid[b] = BEACON
    for pt in all_l1(s, l1(s, b)):
        if pt in grid and grid[pt] is None:
            grid[pt] = CLEAR
    grid.show()

grid.show()

CRIT_Y = 10
opn = [grid[x, CRIT_Y] for x in range(grid.origin[0], grid.origin[0]+grid.width)]
opn_c = opn.count(CLEAR)
opn_b = opn.count(BEACON)
opn_s = opn.count(SENSOR)
print(f'open at {CRIT_Y}: {"".join(chrf(i) for i in opn)}')
print(f'count: {sum((opn_c, opn_b, opn_s))}')
