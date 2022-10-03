import copy
# import numpy as np
import time
import random
import sys
import timeit


def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if 0 <= left == state[compare]:
                print(var, "left", compare)
                return False
            if len(state) > right == state[compare]:
                print(var, "right", compare)
                return False
    return True


def printBoard(state, size):
    output = ''
    row = 0
    for x in range(size ** 2):
        if x % size == 0 and x != 0:
            output += '\n'
            row += 1
        if state[0][row] == x % size:
            output += 'Q '
        else:
            output += '* '
    return output


def getNextUnassignedP1(state):
    return len(state)


def getSortedValuesP1(state, size, row):
    removed = set()
    rList = list(range(0, size))
    for values in rList:
        for val in state:
            x, y = val
            if abs(values - y) == abs(row - x):
                if values not in removed:
                    removed.add(values)
                    break
            if values not in removed and values == y:
                removed.add(values)
                break
    for values in removed:
        rList.remove(values)
    return rList


def cspBackTrackP1(state, size):
    if len(state) == size:
        answer = [y for x, y in state]
        if test_solution(answer):
            return answer
    var = getNextUnassignedP1(state)
    for val in getSortedValuesP1(state, size, var):
        newState = copy.copy(state)
        newState.append((var, val))
        result = cspBackTrackP1(newState, size)
        if result is not None:
            return result
    return None


def getSortedValuesP2(state):
    randomList = state[1]
    if len(state[1]) != 0 and not None:
        randomList = list(state[1])
        random.shuffle(randomList)
    return randomList


def getNextUnassignedP2(state):
    return len(state[0])


def saveCrashRemove(state, remove):
    try:
        state[1].remove(remove)
    except KeyError:
        pass


def cspBackTrackP2(state, size):
    if len(state[0]) == size:
        answer = [y for x, y in state[0]]
        return answer
    var = getNextUnassignedP2(state)
    for val in getSortedValuesP2(state):
        if var - val not in state[2] and var + val not in state[3]:
            newState = [state[0].copy(), state[1].copy(), state[2].copy(), state[3].copy()]
            newState[0].append((var, val))
            saveCrashRemove(newState, val)
            newState[2].add(var - val)
            newState[3].add(var + val)
            result = cspBackTrackP2(newState, size)
            if result is not None:
                return result
    return None


def dictAdd(dictionary, key, value):
    if key in dictionary:
        dictionary[key].add(value)
    else:
        dictionary[key] = {value}


def boardBuilder(state, size):
    for x in range(size):
        if (x * 2) < size and random.randrange(0, size) < size // 2.75:
            temp = x * 2
            state[0].append(temp)
        elif ((x % (size // 2)) * 2) + 1 < size and random.randrange(0, size) < size // 2.75:
            temp = ((x % (size // 2)) * 2) + 1
            state[0].append(temp)
        else:
            temp = (random.randrange(0, size))
            state[0].append(temp)
        dictAdd(state[1], x - temp, x)  # RD
        dictAdd(state[2], x + temp, x)  # LD
        dictAdd(state[3], temp, x)  # C
        state[4].append(set())
    return state


def totalConflictCount(state, printBool):
    total = 0
    for x in state[4]:
        total += len(x)
    if printBool:
        print("Number of Conflicts: %s" % total)
    return total


def conflictCountClean(state, section, num):
    for keys in state[section].keys():
        spot = state[section][keys]
        if num in spot and len(spot) > 1:
            duplicate = copy.copy(spot)
            duplicate.remove(num)
            for i in duplicate:
                state[4][num].add(i)
            break


def conflictCount(state):
    for num, x in enumerate(state[0]):
        conflictCountClean(state, 1, num)
        conflictCountClean(state, 2, num)
        conflictCountClean(state, 3, num)
    totalConflictCount(state, True)


def maxValue(struct):
    maxIndex = []
    maxVal = 0
    for num, x in enumerate(struct):
        if len(x) > maxVal:
            del maxIndex[:]
            maxVal = len(x)
            maxIndex.append(num)
        elif len(x) == maxVal:
            maxIndex.append(num)
    return maxIndex[random.randrange(0, len(maxIndex))]


def dictCheckSafe(dictionary, value):
    try:
        return len(dictionary[value])
    except KeyError:
        return 0


def calcConflicts(state, size):
    moving = maxValue(state[4])
    old = state[0][moving]
    minVal = sys.maxsize
    minValIndex = []
    for x in range(size):
        if x != old:
            val = dictCheckSafe(state[1], moving - x) + dictCheckSafe(state[2], moving + x) + dictCheckSafe(state[3], x)
            if val < minVal:
                del minValIndex[:]
                minVal = val
                minValIndex.append(x)
            elif val == minVal:
                minValIndex.append(x)
    return minValIndex[random.randrange(0, len(minValIndex))], old, moving


def remover(state, qPos, posO):
    try:
        state[1][qPos - posO].remove(qPos)
        state[2][qPos + posO].remove(qPos)
        state[3][posO].remove(qPos)
        for x in state[1][qPos - posO]:
            state[4][x].remove(qPos)
        for x in state[2][qPos + posO]:
            state[4][x].remove(qPos)
        for x in state[3][posO]:
            state[4][x].remove(qPos)
        state[4][qPos].clear()
    except KeyError:
        pass


def adder(state, qPos, posN):
    dictAdd(state[1], qPos - posN, qPos)
    dictAdd(state[2], qPos + posN, qPos)
    dictAdd(state[3], posN, qPos)
    for x in state[1][qPos - posN]:
        if x != qPos:
            state[4][x].add(qPos)
            state[4][qPos].add(x)
    for x in state[2][qPos + posN]:
        if x != qPos:
            state[4][x].add(qPos)
            state[4][qPos].add(x)
    for x in state[3][posN]:
        if x != qPos:
            state[4][x].add(qPos)
            state[4][qPos].add(x)
    state[0][qPos] = posN


def incRepair(state, size):
    print(state[0])
    if totalConflictCount(state, True) != 0:
        posN, posO, qPos = calcConflicts(state, size)
        remover(state, qPos, posO)
        adder(state, qPos, posN)
        incRepair(state, size)
    return state


sys.setrecursionlimit(2000)
start = time.perf_counter()

states = boardBuilder([[], {}, {}, {}, []], 50)
print(states[0])
'''
answer = cspBackTrackP2([[], set(list(range(0, 36))), set(), set()], 36)
print(answer)
test_solution(answer)
print()

answer = cspBackTrackP2([[], set(list(range(0, 38))), set(), set()], 38)
print(answer)
test_solution(answer)
print()

states = boardBuilder([[], {}, {}, {}, []], 50)
conflictCount(states)
incRepair(states, 50)
print(states[0])
test_solution(states[0])
print()

states = boardBuilder([[], {}, {}, {}, []], 56)
conflictCount(states)
incRepair(states, 56)
print(states[0])
test_solution(states[0])
print()
'''

end = time.perf_counter()
print((end - start))
