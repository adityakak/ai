from time import perf_counter
from collections import deque
import heapq
import copy
import sys


def taxicab(board):
    count = 0
    size = len(board) ** 0.5
    goal = find_goal(board)
    for val in board:
        if val != '.':
            x, y = oneTotwo(board.find(val), size)
            xg, yg = oneTotwo(goal.find(val), size)
            count += abs(yg - y) + abs(xg - x)
    return count


def inversionCount(board):
    count = 0
    board = board.replace(".", "")
    copy = board
    for x in board[1:]:
        while copy[int(copy.find(x) - 1)] > x and int(copy.find(x)) - 1 >= 0:
            switch = list(copy)
            hold = switch.index(x)
            temp = switch[hold - 1]
            switch[hold] = temp
            switch[hold - 1] = x
            copy = "".join(switch)
            count += 1
    return count


def parityCheck(board):
    start = perf_counter()
    size = len(board) ** 0.5
    even = size % 2 == 0
    count = inversionCount(board)
    if even:
        x, y = oneTotwo(board.find("."), size)
        if count % 2 == 0:
            if (size - y) % 2 == 0:
                end = perf_counter()
                return False, end - start
        else:
            if (size - y) % 2 == 1:
                end = perf_counter()
                return False, end - start
    else:
        if count % 2 == 1:
            end = perf_counter()
            return False, end - start
    return True, None


def print_puzzle(board, size):
    output = ''
    for i in range(len(board)):
        if i % size == 0 and i > 0:
            output += "\n"
        output += board[i] + " "
    print(output + "\n")


def find_goal(board):
    board = sorted(board)
    board.append(board.pop(0))
    return "".join(board)


def goal_test(test):
    if test == find_goal(test):
        return True
    return False


def swap(list, pos, posSwap):
    list[pos], list[posSwap] = list[posSwap], list[pos]
    return "".join(list)


def twoToOne(x, y, size):
    return int(x + (y * size))


def oneTotwo(index, size):
    return int(index % size), int(index / size)


def get_children(parent):
    children = []
    size = int(len(parent) ** (1 / 2))
    pos = parent.find(".")
    posx, posy = oneTotwo(pos, size)
    if posx + 1 <= size - 1:
        children.append(swap(list(parent), pos, twoToOne(posx + 1, posy, size)))
    if posx - 1 >= 0:
        children.append(swap(list(parent), pos, twoToOne(posx - 1, posy, size)))
    if posy + 1 <= size - 1:
        children.append(swap(list(parent), pos, twoToOne(posx, posy + 1, size)))
    if posy - 1 >= 0:
        children.append(swap(list(parent), pos, twoToOne(posx, posy - 1, size)))
    return children


def bfs(first):
    start = perf_counter()
    mcount = 0
    fringe = deque()
    fringe.append(first)
    visited = {first}
    save = first
    hold = None
    while len(fringe) != 0:
        temp = fringe.popleft()
        if goal_test(temp):
            end = perf_counter()
            return mcount, (end - start)
        if temp == save:
            mcount += 1
            save = None
        for child in get_children(temp):
            if child not in visited:
                hold = child
                fringe.append(child)
                visited.add(child)
        if save is None:
            save = hold
    return None


def DFS(start, k):
    fringe = []
    data = (start, 0, {start})
    fringe.append(data)
    while len(fringe) != 0:
        state, depth, ancestors = fringe.pop()
        if goal_test(state):
            return depth
        if depth < k:
            for child in get_children(state):
                if child not in ancestors:
                    val = copy.copy(ancestors)
                    val.add(child)
                    new_data = (child, depth + 1, val)
                    fringe.append(new_data)
    return None


def IDDFS(start):
    s = perf_counter()
    cap = 0
    result = None
    while result is None:
        result = DFS(start, cap)
        cap += 1
    e = perf_counter()
    return cap - 1, (e - s)


def astar(start):
    s = perf_counter()
    closed = {""}
    data = (taxicab(start), start, 0)
    fringe = []
    heapq.heappush(fringe, data)
    while len(fringe) != 0:
        hueristic, state, depth = heapq.heappop(fringe)
        if goal_test(state):
            e = perf_counter()
            return depth, (e - s)
        if state not in closed:
            closed.add(state)
            for child in get_children(state):
                if child not in closed:
                    new_data = (depth + 1 + taxicab(child), child, depth + 1)
                    heapq.heappush(fringe, new_data)
    return None, None


with open("15_puzzles.txt") as f:
    i = 0
    for line in f:
        moves, time = astar(line.strip())
        print("Line %s: %s, A* - %s moves in %s seconds" % (i, line.strip(), moves, time))
        i += 1
'''
with open(sys.argv[1]) as f:
    i = 0
    for line in f:
        split = line.split()
        solvable, time = parityCheck(split[1])
        if not solvable:
            print("Line %s: %s, no solution determined in %s seconds" % (i, split[1], time))
            print()
        elif split[2] == '!':
            moves, time = bfs(split[1])
            moves2, time2 = IDDFS(split[1])
            moves3, time3 = astar(split[1])
            print("Line %s: %s, BFS - %s moves in %s seconds" % (i, split[1], moves, time))
            print("Line %s: %s, ID-DFS - %s moves in %s seconds" % (i, split[1], moves2, time2))
            print("Line %s: %s, A* - %s moves in %s seconds" % (i, split[1], moves3, time3))
            print()
        elif split[2] == 'B':
            moves, time = bfs(split[1])
            print("Line %s: %s, BFS - %s moves in %s seconds" % (i, split[1], moves, time))
            print()
        elif split[2] == 'I':
            moves, time = IDDFS(split[1])
            print("Line %s: %s, ID-DFS - %s moves in %s seconds" % (i, split[1], moves, time))
            print()
        elif split[2] == 'A':
            moves, time = astar(split[1])
            print("Line %s: %s, A* - %s moves in %s seconds" % (i, split[1], moves, time))
            print()
        i += 1
'''
