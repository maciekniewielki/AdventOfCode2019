import math
import re
from collections import defaultdict

# IO 
formulas =  [re.findall(r"\d+ [A-Z]+", line) for line in open("input.txt").readlines()]
relations = {}
produced = {}
for formula in formulas:
    processed = []
    for x in formula:
        val, name = x.split()
        processed.append((int(val), name))
    in_chemicals, out_chemical = processed[:-1], processed[-1]
    relations[out_chemical[1]] = in_chemicals
    produced[out_chemical[1]] = out_chemical[0]

# 1st
def find_ore(fuel):
    required = [(fuel, 'FUEL')]
    ore = 0 
    got = defaultdict(lambda:0)
    while len(required):
        output = required.pop()
        name = output[1]
        how_much = output[0]
        if got[name] > how_much:
            got[name] -= how_much
            continue
        else:
            how_much -= got[name]
            got[name] = 0
        reaction = relations[name]
        produced_once = produced[name]
        times = math.ceil(how_much / produced_once)
        left = times * produced_once - how_much
        got[name] = left
        for in_chem in reaction:
            if in_chem[1] == 'ORE':
                ore += in_chem[0]*times
            else:
                required.append((times*in_chem[0], in_chem[1]))
    return ore

print(find_ore(1))

# 2nd
ore_for_one_fuel = find_ore(1)
bot = math.floor(1e12 / ore_for_one_fuel)
top = bot*10
while bot != top and bot != top - 1:
    mid = bot + (top-bot) // 2
    if find_ore(mid) > 1e12:
        top = mid
    else:
        bot = mid
print(bot)