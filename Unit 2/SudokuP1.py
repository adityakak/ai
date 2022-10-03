import copy
import time
import random
import sys

N = subH = subW = None
symbolSet = []
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
dictBoard = {}
symbolCount = {}
constraints = {}


def factor(num):
    factors = []
    for j in range(1, num + 1):
        if num % j == 0:
            factors.append(j)
    return factors


def printBoard(state):
    output = ''
    row = 0
    for num in range(len(state)):
        if num != 0 and num % N == 0:
            output += '\n'
            row += 1
        output += state[num] + ' '
    print(output)


def getNextUnassigned(state):
    return state.find('.')


def getSortedValues(state, var):
    numReturn = []
    for num in symbolSet:  # for num in range(1, N + 1):
        boolean = True
        for iterate in range(3):
            if not boolean:
                break
            for val in constraints[var][iterate]:
                if str(num) == state[val]:
                    boolean = False
                    break
        if boolean:
            numReturn.append(num)
    return numReturn


def backtracking(state):
    if state.find('.') == -1:
        return state
    var = getNextUnassigned(state)
    for val in getSortedValues(state, var):
        newState = state[:var] + str(val) + state[var + 1:]
        result = backtracking(newState)
        if result is not None:
            return result
    return None


def findEdge(index):
    x, y = index % N, index // N
    xSpot, ySpot = x // subW, y // subH
    return xSpot * subW, ySpot * subH


#s = time.perf_counter()
#rNum = 0
with open("sudoku_puzzles_1.txt") as f:
    i = 0
    for line in f:
        N = int((len(line) ** .5))
        if N ** .5 == int(N ** .5):
            subH = int(N ** .5)
            subW = int(subH)
        else:
            factors = sorted(factor(N))
            squareRoot = N ** .5
            for x in range(len(factors)):
                if factors[x] < squareRoot < factors[x + 1]:
                    subW = factors[x + 1]
                    subH = factors[x]
                    break
        puzzle = line.strip()
        symbolSet = [str(x) for x in range(1, N + 1) if x < 10]
        if N > 9:
            for i in range(10, N + 1):
                symbolSet.append(alphabet[(i - 10) % N])
        for number in range(len(puzzle)):
            edgeX, edgeY = findEdge(number)
            if puzzle[number] not in symbolCount.keys():
                symbolCount[puzzle[number]] = 1
            else:
                symbolCount[puzzle[number]] += 1
            column = set()
            for x in range(N):
                column.add((x * N) + number % N)
            constraints[number] = [{x for x in range((number // N) * N, ((number // N) * N) + N)}, column,
                                   {x for x in range(edgeX + (edgeY * N), edgeX + subW + ((edgeY + subH) * N)) if
                                    findEdge(x) == (edgeX, edgeY)}]
            constraints[number][0].remove(number)
            constraints[number][1].remove(number)
            constraints[number][2].remove(number)
        answer = backtracking(puzzle)
        print(i, answer)
        i += 1
        #e = time.perf_counter()
        #print(rNum, " ", (e - s))
        #rNum += 1
        #printBoard(answer)
        #print()
