import sys
import os

class Dir:
    def __init__(self):
        self.ents = {}

    def walk(self, path):
        while path.startswith('/'):
            path = path[1:]
        if not path:
            return self
        cmp, sep, rest = path.partition('/')
        ent = self.ents[cmp]
        if sep:
            return ent.walk(rest)
        return ent

class File:
    def __init__(self, sz):
        self.size = sz

wd = '/'
root = Dir()
wde = root

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line.startswith('$ '):
        line = line[2:]
        if line.startswith('cd '):
            dr = line[3:]
            if dr[0] == '/':
                wd = dr
            else:
                wd = os.path.normpath(os.path.join(wd, dr))
        elif line.startswith('ls'):
            print(f'wd: {wd} root: {root.ents}')
            wde = root.walk(wd)
        else:
            raise ValueError(f'Unknown command {line}')
        continue
    sz_or_cls, _, name = line.partition(' ')
    print(sz_or_cls, name)
    if name in wde.ents:
        print(f'WARN: overwriting name {name} in wd {wd}')
    if sz_or_cls == 'dir':
        wde.ents[name] = Dir()
    else:
        wde.ents[name] = File(int(sz_or_cls))

print('Calculating problem results:')
def inorder(pt, wd, deep=0):
    yield pt, wd, deep
    if isinstance(wd, Dir):
        for name, ent in wd.ents.items():
            yield from inorder(os.path.join(pt, name), ent, deep+1)

def calc_size(d):
    running = 0
    for ent in d.ents.values():
        if isinstance(ent, Dir):
            calc_size(ent)
        running += ent.size
    d.size = running

calc_size(root)

for path, ent, deep in inorder('/', root):
    print(f'{" "*deep}- {path} {ent.size}')

LIM = 100000
def prob_spec(d):
    running = 0
    for name, ent in d.ents.items():
        if isinstance(ent, Dir):
            if ent.size <= LIM:
                running += ent.size
            running += prob_spec(ent)
    return running

print(prob_spec(root))
