def calc_fuel(mass, recursive=True):
    fuel = max(mass // 3 - 2, 0)
    if not recursive or not fuel:
        return fuel
    
    return fuel+calc_fuel(fuel)

# IO
masses = list(map(int, open("input.txt").readlines()))

# 1st
print(sum(map(lambda m : calc_fuel(m, False), masses)))

# 2nd
print(sum(map(calc_fuel, masses)))