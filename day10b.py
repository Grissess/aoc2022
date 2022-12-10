import sys

INSN={}
def insn(name):
    def wrap(f):
        INSN[name] = f
        return f
    return wrap

X = 1
CYC = 0
STOP = False
CHECKS = []
def check(f):
    CHECKS.append(f)
    return f

def advance():
    global CYC
    CYC += 1
    for check in CHECKS:
        check()

@insn('noop')
def noop(rest):
    advance()

@insn('addx')
def addx(rest):
    global X
    v = int(rest)
    advance()
    advance()
    X += v

#@check
#def c_prn():
#    print(f'CYC={CYC} X={X}')
#
#SIGSTR = 0
#@check
#def c_sigstr():
#    global SIGSTR, STOP
#    if CYC % 40 == 20:
#        strength = CYC * X
#        print('strength:', strength)
#        SIGSTR += strength
#    if CYC == 220:
#        print("ABORT NOW")
#        STOP = True

@check
def c_render():
    horpos = (CYC - 1) % 40
    if horpos == 0:
        print()
    ch = '#' if abs(X - horpos) <= 1 else '.'
    print(ch, end='', flush=True)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    mne, _, rest = line.partition(' ')
    op = INSN.get(mne, None)
    if op is None:
        print('WARN: bad opcode', mne)
        continue
    op(rest)
    if STOP:
        break

print('total:', SIGSTR)
