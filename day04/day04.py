# IO
r = (353096,843212)


def check1(n):
    d = list(map(int, str(n)))
    prev = d[0]
    same = False
    for x in d[1:]:
        if x == prev:
            same = True
        if x<prev:
            return False
        prev = x
    return same


def check2(n):
    d = list(map(int, str(n)))
    prev = d[0]

    for x in d[1:]:
        if x<prev:
            return False
        prev = x
    
    if d[0] == d[1] and d[1] != d[2]:
        return True

    if d[0] != d[1] and d[1] == d[2] and d[2] != d[3]:
        return True
        
    if d[1] != d[2] and d[2] == d[3] and d[3] != d[4]:
        return True

    if d[2] != d[3] and d[3] == d[4] and d[4] != d[5]:
        return True
    
    if d[3] != d[4] and d[4] == d[5]:
        return True


    return False


# 1st
print(sum([check1(x) for x in range(*r)]))

# 2nd
print(sum([check2(x) for x in range(*r)]))