import sys

lt_cls = lambda x: ord(x) - ord('A')
rt_cls = lambda x: ord(x) - ord('X')
def dom(a, b):
    res = (a - b) % 3
    if res == 2:
        res = -1
    if res == -2:
        res = 1
    return res

running = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    lt, _, rt = line.partition(' ')
    lc, rs = lt_cls(lt), rt_cls(rt)
    rc = (lc + rs - 1) % 3
    sco = (rc + 1) + 3 * (dom(rc, lc) + 1)
    print(sco)
    running += sco
print(running)
