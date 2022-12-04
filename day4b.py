import sys

def intv(x):
    l, _, h = x.partition('-')
    return int(l), int(h)

def olap(il, ih, ol, oh):
    return il >= ol and ih <= oh

def isct(al, ah, bl, bh):
    l = max(al, bl)
    h = min(ah, bh)
    return l <= h

running = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    l, _, r = line.partition(',')
    ll, lh = intv(l)
    rl, rh = intv(r)
    #if olap(ll, lh, rl, rh) or olap(rl, rh, ll, lh):
    if isct(ll, lh, rl, rh):
        running += 1

print(running)

