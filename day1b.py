import sys

sums = []
running = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        sums.append(running)
        running = 0
        continue
    running += int(line)

sums.append(running)
print(sums)
sums.sort()
top = sums[-3:]
print(top)
print(sum(top))
