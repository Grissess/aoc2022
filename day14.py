import sys

SOURCE = (500, 0)
WALL, SAND, PATH, ORIGIN = [object() for _ in range(4)]

def chrf_sand(o):
    if o is None:
        return '.'
    if o is WALL:
        return '#'
    if o is SAND:
        return 'o'
    if o is PATH:
        return '~'
    if o is ORIGIN:
        return '+'
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
        return 0 <= self.co(*pr) < len(self.data)

    def __getitem__(self, pr):
        (x, y) = pr
        return self.data[self.co(x, y)]

    def __setitem__(self, pr, v):
        (x, y) = pr
        self.data[self.co(x, y)] = v

    def show(self, chrf=chrf_sand):
        ox, oy = self.origin
        for y in range(self.height):
            for x in range(self.width):
                print(f'{chrf(self[x+ox, y+oy])}', end='')
            print()
        print()

strokes = []
pts = [SOURCE]
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    points = line.split(' -> ')
    for i, p in enumerate(points):
        x, _, y = p.partition(',')
        points[i] = (int(x), int(y))
    for s, e in zip(points, points[1:]):
        pts.extend((s, e))
        strokes.append((s, e))

xs, ys = [p[0] for p in pts], [p[1] for p in pts]
xmn, xmx, ymn, ymx = min(xs), max(xs), min(ys), max(ys)
dx, dy = xmx - xmn + 3, ymx - ymn + 3
print(f'size ({dx}, {dy}), origin ({xmn}, {ymn}), extent ({xmx}, {ymx})')
grid = Grid(dx, dy, (xmn - 1, ymn - 1))

def tween(a, b):
    l, h = min(a, b), max(a, b)
    return range(l, h+1)

for s, e in strokes:
    print(f'plot {s} -> {e}')
    sx, sy = s
    ex, ey = e
    assert sx == ex or sy == ey
    if sx == ex:
        for y in tween(sy, ey):
            grid[sx, y] = WALL
    else:
        for x in tween(sx, ex):
            grid[x, sy] = WALL

grid[SOURCE] = ORIGIN
grid.show()

def sim_sand(p, pth=()):
    npth = pth + (p,)
    if p not in grid:
        return None, pth
    x, y = p
    nxt = ((x, y+1), (x-1, y+1), (x+1, y+1))
    saw_grid = False
    for cand in nxt:
        if cand not in grid:
            continue
        saw_grid = True
        if grid[cand] is None:
            return sim_sand(cand, npth)
    if not saw_grid:
        return None, npth
    return p, npth

counter = 0
while True:
    part, pth = sim_sand(SOURCE)
    if part is None:
        for pt in pth:
            grid[pt] = PATH
        break
    counter += 1
    grid[part] = SAND
    #grid.show()

grid.show()
print('produced:', counter, 'particles')
