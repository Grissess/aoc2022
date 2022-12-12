import sys, time

htf = lambda x: 0 if x == 'S' else 25 if x == 'E' else ord(x) - ord('a')

hm = []
sp = None
ep = None

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    hm.append([htf(i) for i in line])
    if 'S' in line:
        sp = (line.index('S'), len(hm) - 1)
    if 'E' in line:
        ep = (line.index('E'), len(hm) - 1)

height, width = len(hm), len(hm[0])

def in_board(v):
    x, y = v
    return 0 <= x < width and 0 <= y < height

def height_of(v):
    x, y = v
    return hm[y][x]

def ortho_neighf(v):
    x, y = v
    h = height_of(v)
    return [
            cand
            for cand in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            if in_board(cand) and height_of(cand) <= h + 1
    ]

def srch(start, goal, neighf, edgef=lambda l, r: 1, refresh=10):
    queue = [start]
    cost = {start: 0}
    back = {}
    explored = set()
    counter = 0
    #print('\x1b[1;31m', end='')

    while queue:
        here = queue.pop(0)
        cost_here = cost[here]
        explored.add(here)
        x, y = here
        #print(f'\x1b[{y+1};{x+1}H{chr(ord("a")+height_of(here))}', end='')
        if counter % refresh == 0:
            sys.stdout.flush()
            #time.sleep(0.01)
        counter += 1
        if here == goal:
            path = []
            vert = here
            while vert in back:
                path.append(vert)
                vert = back[vert]
            path.append(start)
            return cost_here, list(reversed(path))
        for reach in neighf(here):
            weight = edgef(here, reach)
            total_cost = cost_here + weight
            if reach not in cost or cost[reach] > total_cost:
                cost[reach] = total_cost
                back[reach] = here
            if reach not in explored and reach not in queue:
                queue.append(reach)
        queue.sort(key=lambda v: cost[v])

print('\x1b[2J\x1b[H', end='')
for y in range(height):
    for x in range(width):
        print(chr(ord('a') + hm[y][x]), end='')
    print()

print('\x1b[1;31m', end='')
min_res = None
counter = 0
for y in range(height):
    for x in range(width):
        if hm[y][x] != 0:
            continue
        print(f'\x1b[{y+1};{x+1}H{chr(ord("a") + hm[y][x])}', end='')
        if counter % 100 == 0:
            sys.stdout.flush()
        counter += 1
        res = srch((x, y), ep, ortho_neighf)
        if res:
            if min_res is None or res[0] < min_res[0]:
                min_res = res

res = min_res
print(f'\x1b[{height+1}H')
if res is None:
    print('No path')
else:
    cst, pth = res
    print('cost:', cst)
    print('path:', pth)
    print('len:', len(pth))
