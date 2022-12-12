import sys

class Item:
    def __init__(self, worry):
        self.worry = worry

    def turn_worry(self):
        self.worry //= 3

class Monkey:
    def __init__(self, ident):
        self.ident = ident
        self.queue = []
        self.operator = None
        self.test = None
        self.targets = [None, None]
        self.inspections = 0

    def thread(self, mapping):
        for tidx, tgt in enumerate(self.targets):
            self.targets[tidx] = mapping[tgt]

    def turn(self):
        print('monkey', self.ident)
        q = self.queue[:]
        self.inspections += len(q)
        self.queue = []
        for item in q:
            print('\tinspect:', item.worry)
            item.worry = self.operator(item.worry)
            print('\t\tnow:', item.worry)
            item.turn_worry()
            print('\t\tdec:', item.worry)
            target = self.targets[self.test(item.worry)]
            print('\ttarget:', target.ident)
            target.queue.append(item)

cur_monkey = None
all_monkeys = {}
ordering = []

TEST_BUILDERS = {}
def test_builder(name):
    def wrap(f):
        TEST_BUILDERS[name] = f
        return f
    return wrap

@test_builder('divisible')
def divisible(rest):
    _, _, by = rest.partition(' ')
    return lambda v, by=int(by): v % by == 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    if line.startswith('Monkey'):
        _, _, ident = line.partition(' ')
        ident = ident[:-1]
        cur_monkey = Monkey(ident)
        all_monkeys[ident] = cur_monkey
        ordering.append(ident)
    elif line.startswith('Starting items'):
        _, _, rest = line.partition(':')
        items = [Item(int(w.strip())) for w in rest.split(',') if w.strip()]
        cur_monkey.queue.extend(items)
    elif line.startswith('Operation'):
        _, _, func = line.partition(':')
        loc = {}
        src = f'def operation(old):\n  {func.strip()}\n  return new\n'
        print('src:\n', src)
        exec(src, globals(), loc)
        cur_monkey.operator = loc['operation']
    elif line.startswith('Test'):
        _, _, test = line.partition(':')
        test = test.strip()
        name, _, rest = test.partition(' ')
        builder = TEST_BUILDERS[name]
        cur_monkey.test = builder(rest)
    elif line.startswith('If'):
        _, _, cond = line.partition(' ')
        idx = cond.startswith('true')
        tgt = cond.split()[-1]
        cur_monkey.targets[idx] = tgt

for monkey in all_monkeys.values():
    monkey.thread(all_monkeys)

for rnd in range(20):
    for ident in ordering:
        monkey = all_monkeys[ident]
        monkey.turn()

monkeys_sorted = list(all_monkeys.values())
monkeys_sorted.sort(key=lambda m: m.inspections)
for m in monkeys_sorted:
    print(m.ident, ':', m.inspections)
