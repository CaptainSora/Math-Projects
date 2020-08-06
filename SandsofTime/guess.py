from itertools import combinations_with_replacement

TIME = [4, 7]

def duration(planstr, verbose=False):
    # Input must be delimited with commas for instructions
    duration = 0
    glass1 = 0
    glass2 = 0
    plan = planstr.split(', ')
    while True:
        if verbose:
            print(duration, glass1, glass2)
        if not plan and glass1 == 0 and glass2 == 0:
            return duration, duration % TIME[0]
        end = [glass1 == 1, glass2 == 1]
        if glass1 or glass2:
            glass1 = max(0, glass1 - 1)
            glass2 = max(0, glass2 - 1)
            duration += 1
        if duration == 0 or any(end) and plan:
            flip = plan.pop(0).split('/')
            if str(TIME[0]) in flip:
                glass1 = TIME[0] - glass1
            if str(TIME[1]) in flip:
                glass2 = TIME[1] - glass2

# print(duration('7/11, 7, 11, 7'))

best = [['', 0]] * TIME[0]
for i in range(10):
    for c in combinations_with_replacement(TIME, i):
        base = [f'{TIME[0]}/{TIME[1]}']
        base.extend(c)
        order = ', '.join([str(x) for x in base])
        dur, mod = duration(order)
        if best[mod][0] == '' or best[mod][1] > dur:
            best[mod] = [order, dur]

highest = 0
for i in range(len(best)):
    highest = max(highest, best[i][1])
    print(f"{best[i][1]} ({i} mod {TIME[0]}) || {best[i][0]} ||")
print(f"Current Record: {highest - TIME[0]}")