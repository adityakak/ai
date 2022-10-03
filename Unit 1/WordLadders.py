from time import perf_counter
from collections import deque
import sys

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]


def get_children(parent):
    children = []
    for a in range(len(parent)):
        p = list(parent)
        for x in range(26):
            p[a] = alphabet[x]
            s = "".join(p)
            if s in dictionary and s != parent:
                children.append(s)
    return children


def path(parent, s, e):
    ptake = []
    child = e
    while child != s:
        ptake.append(child)
        child = parent[child]
    ptake.append(child)
    ptake.reverse()
    return ptake


def bfs(s, e):
    count = 0
    fringe = deque()
    fringe.append(s)
    visited = {s}
    save = s
    hold = None
    while len(fringe) != 0:
        temp = fringe.popleft()
        if temp == e:
            return count
        if temp == save:
            count += 1
            save = None
        for child in get_children(temp):
            if child not in visited:
                hold = child
                fringe.append(child)
                visited.add(child)
        if save is None:
            save = hold
    return None


with open(sys.argv[2]) as f:
    line_list = [line.strip() for line in f]
    ladder_pair = [x.split() for x in line_list]
with open(sys.argv[1]) as f:
    start = perf_counter()
    i = 1
    dictionary = {}
    for line in f:
        dictionary[line.strip()] = i
        i += 1
    end = perf_counter()
    print("Time to create data structure was: %s seconds" % (end - start))
    print("There are %s words in this dict." % i)
i = 0
total_time = 0
for x in ladder_pair:
    print()
    print("Line %s" % i)
    start = perf_counter()
    moves = bfs(x[0], x[1])
    end = perf_counter()
    total_time += (end - start)
    if moves is None:
        print("No Solution!")
    else:
        print("Length is: %s" % (moves + 1))
        #for z in l:
        #    print(z)
    i += 1


print()
print("Time to solve all of these puzzles was: %s seconds" % total_time)
