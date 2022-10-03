from time import perf_counter
from collections import deque
import sys

parent = []
children = []


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
    size = len(board) ** 0.5
    even = size % 2 == 0
    count = inversionCount(board)
    if even:
        x, y = oneTotwo(board.find("."), size)
        if count % 2 == 0:
            if (size - y) % 2 == 0:
                return False
        else:
            if (size - y) % 2 == 1:
                return False
    else:
        if count % 2 == 1:
            return False
    return True


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



with open(sys.argv[1]) as f:
    i = 0
    for line in f:
        split = line.strip()
        moves, time = bfs(split)
        print("Line %s: %s, %s moves found in %s seconds" % (i, split, moves, time))
        i += 1

