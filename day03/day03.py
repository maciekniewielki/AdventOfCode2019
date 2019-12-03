# IO
moves = list( open("input.txt").readlines())
moves1 = moves[0].split(",")
moves2 = moves[1].split(",")

def manhattan(point):
    return abs(point[0])+abs(point[1])


def traverse(moves):
    pos = [0, 0]
    visited = {}
    steps_done = 0
 
    for move in moves:
        if not move:
            continue
        where = move[0]
        howmuch = int("".join(move[1:]))
        for _ in range(howmuch):
            if where == "U":
                pos[1]+=1
            elif where == "D":
                pos[1]-=1
            elif where == "L":
                pos[0]-=1
            elif where == "R":
                pos[0]+=1
            steps_done += 1
            
            point = tuple(pos)
            if point not in visited:
                visited[point] = steps_done

    return visited

path1 = traverse(moves1)
path2 = traverse(moves2)
shared = set(path1.keys()).intersection(set(path2.keys()))

# 1st
print(min(manhattan(p) for p in shared))

#2nd
print(min(path1[p]+path2[p] for p in shared))
