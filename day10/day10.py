import math
# IO 
a = [x[:-1] for x in open("input.txt").readlines()]
w = len(a[0])
h = len(a)

def construct_line(a, b):
    if a[0] == b[0]:
        return (1, 0, a[0])
    elif a[1] == b[1]:
        return (0, 1, a[1])
    
    return (a[1]-b[1], b[0]-a[0], (b[0]-a[0])*a[1]+(a[1]-b[1])*a[0])


def check_if_in_line(a, line):
    if a[0] * line[0] + a[1] * line[1] == line[2]:
        return True
    return False

def double_for(w, h):
    for x in range(w):
        for y in range(h):
            yield x,y

def check_any_in_line(a1, a2, line):
    x1 = min(a1[0], a2[0])
    x2 = max(a1[0], a2[0])
    y1 = min(a1[1], a2[1])
    y2 = max(a1[1], a2[1])
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if a[y][x] == ".":
                continue
            if (x,y) == a2 or (x,y) == a1:
                continue
            if check_if_in_line((x,y), line):
                return True
    return False

def get_asteroids_in_range(a1):
    x1, y1 = a1
    asteroids_in_range = set()
    asteroids_in_range.add((x1,y1))
    for x2, y2 in double_for(w, h):
        if a[y2][x2] == ".":
            continue
        if (x2,y2) == (x1, y1):
            continue
        line = construct_line((x1,y1), (x2,y2))
        if check_any_in_line((x1,y1), (x2,y2), line):
            continue
        asteroids_in_range.add((x2, y2))
    return asteroids_in_range


def angle(a1, a2):
    x2, y2 = a2[0]-a1[0], a2[1]-a1[1]
    return math.atan2(x2, y2)

def angle_corrected(a1, a2):
    pi = 3.1415926535
    if a1[0] == a2[0]:
        if a1[1] > a2[1]:
            return 0
        else:
            return pi
    a = angle(a1, a2)
    if a < 0:
        return pi - a
    return a

# 1st
asteroids_in_range = {}

for x1,y1 in double_for(w, h):
    if a[y1][x1] == ".":
        continue
    asteroids_in_range[(x1,y1)] = get_asteroids_in_range((x1, y1))
best = max(asteroids_in_range, key=lambda x: len(asteroids_in_range[x]))
print(len(asteroids_in_range[best])-1)

# 2nd
visible = asteroids_in_range[best]
visible.remove(best)
asteroid200 = list(sorted(list(visible), key=lambda a2: angle_corrected(best, a2)))[199]
print(asteroid200[0]*100+asteroid200[1])


        

        