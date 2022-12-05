import sys
import re

stacks = []

def pprint(stks):
    maxlen = max([len(i) for i in stks])

    for ix in range(maxlen, -1, -1):
        for stk in stks:
            if ix < len(stk):
                print(f'[{stk[ix]}] ', end='')
            else:
                print('    ', end='')
        print()

    for i in range(len(stks)):
        print(f' {i+1}  ', end='')
    print()

mvmt = re.compile(r'move (\d+) from (\d+) to (\d+)')

for line in sys.stdin:
    line = line.rstrip()
    if not line:
        continue

    if line.startswith('move'):
        mo = mvmt.match(line)
        amt, frm, to = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
        print(f'amt={amt}, frm={frm}, to={to}')
        pprint(stacks)
        #taken = stacks[frm - 1][-amt:]
        #if len(taken) < amt:
        #    print(f'WARN: cannot take {amt} from stack {frm} ({stacks[frm - 1]})')
        #if amt == len(stacks[frm - 1]):
        #    stacks[frm - 1] = []
        #else:
        #    stacks[frm - 1] = stacks[frm - 1][:amt + 1]
        #stacks[to - 1].extend(reversed(taken))
        temp = []
        for i in range(amt):
            temp.append(stacks[frm - 1].pop())
        stacks[to - 1].extend(reversed(temp))
        continue

    lim = (len(line) // 4) + 1
    print(f'len(line)={len(line)}, lim={lim}')
    for i in range(lim):
        part = line[4*i:4*(i+1)]
        if not part:
            break
        print(f'i={i}, part={part!r}')
        if part[1].isdigit():
            break  # just the indicator line
        if part[1].isspace():
            continue
        while len(stacks) <= i:
            stacks.append([])
        stacks[i].insert(0, part[1])
    print('nextl')

pprint(stacks)

for stk in stacks:
    print(stk[-1], end='')
print()
