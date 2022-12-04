import sys

priority = lambda x: ord(x) - ord('a') + 1 if x.islower() else ord(x) - ord('A') + 27

running = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    div = len(line) // 2
    l, r = set(line[:div]), set(line[div:])
    isc = l & r
    print(isc)
    common = list(isc)[0]
    pri = priority(common)
    print(pri)
    running += pri
print(running)
