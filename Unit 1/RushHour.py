from time import perf_counter
from collections import deque
import heapq
import sys
import copy
import numpy as np

alphabet = ['A', 'B', 'C', 'D', 'E', 'f', 'G', 'H', 'I', 'J', 'K']


def print_puzzle(board):
    grid = ""
    index = 0
    for value in board:
        index += 1
        grid += value + " "
        if index % 6 == 0:
            grid += "\n"
    print(grid)


def twoToOne(x, y, size):
    return x + (y * size)


def oneTotwo(index, size):
    return index % size, index // size


def move(edge, originalEdge, originalEdge2, boolean, secondD, state):
    change = list(state)
    if boolean:
        for i in range(edge, edge + (originalEdge2 - originalEdge)):
            swap = twoToOne(i, secondD, 6)
            original = twoToOne(i - edge + originalEdge, secondD, 6)
            change[swap], change[original] = change[original], change[swap]
    else:
        for i in range(edge, edge + (originalEdge2 - originalEdge)):
            swap = twoToOne(secondD, i, 6)
            original = twoToOne(secondD, i - edge + originalEdge, 6)
            change[swap], change[original] = change[original], change[swap]
    return "".join(change)


def lengthClear(edge, length, secondD, boolean, char, state):
    for i in range(edge, edge + length):
        if boolean:
            if state[twoToOne(i, secondD, 6)] != '.' and state[twoToOne(i, secondD, 6)] != char:
                return False
        else:
            if state[twoToOne(secondD, i, 6)] != '.' and state[twoToOne(secondD, i, 6)] != char:
                return False
    return True


def get_children(parent, cars):
    children = []
    car = []
    for i in range(cars):
        posSx, posSy = oneTotwo(parent.index(alphabet[i]), 6)
        posFx, posFy = oneTotwo(parent.rfind(alphabet[i]), 6)
        if abs(posFx > posSx):
            car.append((posSx, posFx, posSy, True))
        else:
            car.append((posSy, posFy, posSx, False))
        print(car[i])
    count = 0
    for i in car:
        char = alphabet[count]
        one, two, third, row = i
        for j in range(0, one):
            if lengthClear(j, two - one, third, row, char, parent):
                children.append(move(j, one, two, row, third, parent))
            else:
                break
        for j in range(two + 1, 6):
            if lengthClear(j, two - one, third, row, char, parent):
                children.append(move(j, one, two, row, third, parent))
            else:
                break
        count += 1


# y is rows x is column
s = 'ABCCD.ABEED.ffGH....GHI...JHI...J...'
print_puzzle(s)
get_children(s, 10)
