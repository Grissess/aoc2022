import sys, functools, operator

priority = lambda x: ord(x) - ord('a') + 1 if x.islower() else ord(x) - ord('A') + 27

running = 0
obs = []
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    obs.append(set(line))
    if len(obs) == 3:
        common = functools.reduce(operator.and_, obs)
        assert len(common) == 1
        common = list(common)[0]
        del obs[:]
    else:
        continue
    pri = priority(common)
    print(pri)
    running += pri
print(running)
