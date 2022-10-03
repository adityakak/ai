import time, sys, copy
from operator import itemgetter
import random

height = 0
width = 0
numBlocking = 0
words = set()


def start():
    sizes = arguments[1]
    global height, width, numBlocking
    xPosition = sizes.find('x')
    height = int(sizes[:xPosition])
    width = int(sizes[xPosition + 1:])

    numBlocking = int(arguments[2])
    with open(arguments[3]) as f:
        for line in f:
            line = line.strip()
            if line.isalpha():
                words.add(line)
    state = ''
    for i in range(height * width):
        state += '-'
    # printBoard(state)
    placedList = set()
    blocksPlacedList = set()
    for i in range(4, len(arguments)):
        inputLocation = arguments[i]
        xPosition = inputLocation.find('x')
        startOfWord = 0
        for characters in range(xPosition + 1, len(inputLocation)):
            if inputLocation[characters].isalpha() or inputLocation[characters] == '#':
                startOfWord = characters
                break
        loc = int(inputLocation[xPosition + 1: startOfWord]) + (int(inputLocation[1:xPosition]) * width)
        word = inputLocation[startOfWord:]
        if inputLocation[0] == 'H':
            for num, j in enumerate(word):
                state = state[:loc + num] + j + state[loc + num + 1:]
                if j == '#':
                    blocksPlacedList.add(loc + num)
                else:
                    placedList.add(loc + num)
        else:
            for num, j in enumerate(word):
                state = state[:loc + (num * width)] + j + state[loc + (num * width) + 1:]
                if j == '#':
                    blocksPlacedList.add(loc + (num * width))
                else:
                    placedList.add(loc + (num * width))
    return state, placedList, blocksPlacedList
    """
    sizes = sys.argv[1]
    global height, width, numBlocking
    xPosition = sizes.find('x')
    height = int(sizes[:xPosition])
    width = int(sizes[xPosition + 1:])

    numBlocking = int(sys.argv[2])
    with open(sys.argv[3]) as f:
        for line in f:
            line = line.strip()
            if line.isalpha():
                words.add(line)
    state = ''
    for i in range(height * width):
        state += '-'
    # printBoard(state)
    placedList = set()
    blocksPlacedList = set()
    for i in range(4, len(sys.argv)):
        inputLocation = sys.argv[i]
        xPosition = inputLocation.find('x')
        startOfWord = 0
        for characters in range(xPosition + 1, len(inputLocation)):
            if inputLocation[characters].isalpha() or inputLocation[characters] == '#':
                startOfWord = characters
                break
        loc = int(inputLocation[xPosition + 1: startOfWord]) + (int(inputLocation[1:xPosition]) * width)
        word = inputLocation[startOfWord:]
        if inputLocation[0] == 'H' or inputLocation[0] == 'h':
            for num, j in enumerate(word):
                state = state[:loc + num] + j + state[loc + num + 1:]
                if j == '#':
                    blocksPlacedList.add(loc + num)
                else:
                    placedList.add(loc + num)
        else:
            for num, j in enumerate(word):
                state = state[:loc + (num * width)] + j + state[loc + (num * width) + 1:]
                if j == '#':
                    blocksPlacedList.add(loc + (num * width))
                else:
                    placedList.add(loc + (num * width))
    return state, placedList, blocksPlacedList
    """


def fixMaxes(state, dimension, loc):
    if dimension:
        streak = maxStreak = s = tempS = e = 0
        for i in range(height):
            pos = loc + (width * i)
            if state[pos] == '-' and streak == 0:
                tempS = pos
                streak += 1
            elif state[pos] == '-' and streak > 0:
                streak += 1
            else:
                streak = 0
            if streak > maxStreak:
                maxStreak = streak
                s = tempS
                e = pos
        return maxStreak, s, e
    else:
        streak = maxStreak = s = tempS = e = 0
        for i in range(width):
            pos = i + (width * loc)
            if state[pos] == '-' and streak == 0:
                tempS = pos
                streak += 1
            elif state[pos] == '-' and streak > 0:
                streak += 1
            else:
                streak = 0
            if streak > maxStreak:
                maxStreak = streak
                s = tempS
                e = pos
        return maxStreak, s, e



def connectednessHelper(state, pos):
    state = state[:pos] + '*' + state[pos + 1:]
    x, y = pos % width, pos // width
    dir2 = x + ((y + 1) * width)  # Down
    dir1 = x + ((y - 1) * width)  # Up
    if 0 <= dir1 <= (width * height) - 1 and state[dir1] != '#' and state[dir1] != '*':
        state = connectednessHelper(state, dir1)
    if 0 <= dir2 <= (width * height) - 1 and state[dir2] != '#' and state[dir2] != '*':
        state = connectednessHelper(state, dir2)
    if x + 1 < width:
        dir4 = (x + 1) + (y * width)  # Right
        if 0 <= dir4 <= (width * height) - 1 and state[dir4] != '#' and state[dir4] != '*':
            state = connectednessHelper(state, dir4)
    if x - 1 >= 0:
        dir3 = (x - 1) + (y * width)  # Left
        if 0 <= dir3 <= (width * height) - 1 and state[dir3] != '#' and state[dir3] != '*':
            state = connectednessHelper(state, dir3)
    return state


def connectedness(state):
    for pos, item in enumerate(state):
        if item.isalpha():
            state = state[:pos] + '-' + state[pos + 1:]
    savePos = 0
    for num, item in enumerate(state):
        if item == '-':
            savePos = num
            break
    state = connectednessHelper(state, savePos)
    for item in state:
        if item != '#' and item != '*':
            return False, state
    return True, state


def allows3(state, pos1, pos2):
    toCheck = [pos1, pos2]
    for item in toCheck:
        col, row = item % width, item // width
        # Up
        freeSpace = 0
        for i in range(1, 4):
            newPos = col + ((row - i) * width)
            if i == 1 and newPos < 0:
                break
            elif i != 1 and newPos < 0:
                return False
            character = state[newPos]
            if character == '-' or character.isalpha():
                freeSpace += 1
                continue
            if i == 1 and (character == '#' or character.isalpha()):
                break
        if 0 < freeSpace < 3:
            return False
        # Down
        freeSpace = 0
        for i in range(1, 4):
            newPos = col + ((row + i) * width)
            if i == 1 and newPos >= (height * width):
                break
            elif i != 1 and newPos >= (height * width):
                return False
            character = state[newPos]
            if character == '-' or character.isalpha():
                freeSpace += 1
                continue
            if i == 1 and (character == '#' or character.isalpha()):
                break
        if 0 < freeSpace < 3:
            return False
        # Right
        freeSpace = 0
        for i in range(1, 4):
            if i == 1 and col + i >= width:
                break
            if i != 1 and col + i >= width:
                return False
            newPos = (col + i) + (row * width)
            character = state[newPos]
            if character == '-' or character.isalpha():
                freeSpace += 1
                continue
            if i == 1 and (newPos >= (height * width) or character == '#' or character.isalpha()):
                break
        if 0 < freeSpace < 3:
            return False
        # Left
        freeSpace = 0
        for i in range(1, 4):
            if i == 1 and col - i < 0:
                break
            if i != 1 and col - i < 0:
                return False
            newPos = (col - i) + (row * width)
            character = state[newPos]
            if character == '-' or character.isalpha():
                freeSpace += 1
                continue
            if i == 1 and (newPos < 0 or character == '#' or character.isalpha()):
                break
        if 0 < freeSpace < 3:
            return False
    return True


def subdivideHorz(state, loc, placedLetters, placedBlocks):
    possible = []
    for i in range(width):
        pos = i + (width * loc)  # Check all for directions for closeness
        oppPos = (width - i - 1) + ((height - loc - 1) * width)
        if pos == oppPos:
            continue
        if pos in placedLetters or pos in placedBlocks or oppPos in placedLetters or oppPos in placedBlocks:
            continue
        newState = state[:pos] + '#' + state[pos + 1:]
        newState = newState[:oppPos] + '#' + newState[oppPos + 1:]
        tempBlocks = placedBlocks.copy()
        tempBlocks.add(pos)
        tempBlocks.add(oppPos)
        newState, tempBlocks, needCheck = filler(newState, tempBlocks)
        allowed = True
        if allows3(newState, pos, oppPos):
            for item in needCheck:
                if not allows3(newState, item[0], item[1]):
                    allowed = False
                    break
            if allowed: possible.append((newState, tempBlocks.copy(), pos, oppPos))
    refinedPossible = []
    for item in possible:
        newState, temps, pos, oppPos = item
        check, vals = connectedness(newState)
        if check:
            refinedPossible.append((newState, temps.copy(), pos, oppPos))
    return refinedPossible


def subdivideVert(state, loc, placedLetters, placedBlocks):
    possible = []
    for i in range(height):
        pos = loc + (width * i)  # Check all for directions for closeness
        oppPos = (width - loc - 1) + ((height - i - 1) * width)
        if pos == oppPos:
            continue
        if pos in placedLetters or pos in placedBlocks or oppPos in placedLetters or oppPos in placedBlocks:
            continue
        newState = state[:pos] + '#' + state[pos + 1:]
        newState = newState[:oppPos] + '#' + newState[oppPos + 1:]
        tempBlocks = placedBlocks.copy()
        tempBlocks.add(pos)
        tempBlocks.add(oppPos)
        newState, tempBlocks, needCheck = filler(newState, tempBlocks)
        allowed = True
        if allows3(newState, pos, oppPos):
            for item in needCheck:
                if not allows3(newState, item[0], item[1]):
                    allowed = False
                    break
            if allowed: possible.append((newState, tempBlocks.copy(), pos, oppPos))
    refinedPossible = []
    for item in possible:
        newState, temps, pos, oppPos = item
        check, vals = connectedness(newState)
        if check:
            refinedPossible.append((newState, temps.copy(), pos, oppPos))
    return refinedPossible


def getNextUnassigned(direction, vert, horz):
    indexList = []
    if direction:
        vert2 = sorted(vert, key=lambda tup: tup[0], reverse=True)
        for item in vert2:
            indexList.append(vert.index(item))
    else:
        horz2 = sorted(horz, key=lambda tup: tup[0], reverse=True)
        for item in horz2:
            indexList.append(horz.index(item))
    return indexList


def getSortedValues(state, pos, dimension, placedLetters, placedBlocks):
    if dimension:
        return subdivideVert(state, pos, placedLetters, placedBlocks)
    else:
        return subdivideHorz(state, pos, placedLetters, placedBlocks)


def fixData(state, pos1, pos2, horz, vert, placedBlocks):
    x, y = pos1 % width, pos1 // width
    tempVert = fixMaxes(state, True, x)
    tempHorz = fixMaxes(state, False, y)
    vert[x] = tempVert
    horz[y] = tempHorz
    x, y = pos2 % width, pos2 // width
    tempVert = fixMaxes(state, True, x)
    tempHorz = fixMaxes(state, False, y)
    vert[x] = tempVert
    horz[y] = tempHorz
    placedBlocks.add(pos1)
    placedBlocks.add(pos2)
    return horz, vert, placedBlocks


def blockCounter(state):
    count = 0
    for item in state:
        if item == '#':
            count += 1
    return count


def fill(state, where, placed):
    newAdds = []
    s, e, direction = where
    if direction == 0:
        step = -1 * width
    elif direction == 1:
        step = width
    elif direction == 2:
        step = 1
    else:
        step = -1
    for i in range(s, e, step):
        col, row = i % width, i // width
        oppPos = (width - col - 1) + ((height - row - 1) * width)
        if not state[i].isalpha() and not state[oppPos].isalpha():
            state = state[:i] + '#' + state[i + 1:]
            state = state[:oppPos] + '#' + state[oppPos + 1:]
            newAdds.append((i, oppPos))
        placed.add(i)
        placed.add(oppPos)
    return state, placed, newAdds


def fixFill(state, checkstate, placed):
    newAdds = []
    replace = []
    for num, item in enumerate(checkstate):
        if item == '-':
            replace.append(num)
    for item in replace:
        col, row = item % width, item // width
        oppPos = (width - col - 1) + ((height - row - 1) * width)
        if not state[item].isalpha() and not state[oppPos].isalpha():
            state = state[:item] + '#' + state[item + 1:]
            state = state[:oppPos] + '#' + state[oppPos + 1:]
            newAdds.append((item, oppPos))
        placed.add(item)
        placed.add(oppPos)
    return state, placed, newAdds


def fillerHelper(state, pos1, pos2, direction, placed, addsExtend, unionExtend):
    state, placedTemp, newTemp = fill(state, (pos1, pos2, direction), placed.copy())
    addsExtend.extend(newTemp)
    unionExtend.update(placedTemp)
    check, checkState = connectedness(state)
    if not check:
        state, placedTemp, newTemp = fixFill(state, checkState, placed.copy())
        addsExtend.extend(newTemp)
        unionExtend.update(placedTemp)
    return state, addsExtend, unionExtend


def filler(state, placed):
    unionizer = set()
    newAdds = []
    for item in placed:
        col, row = item % width, item // width
        streak = 0
        for j in range(1, 4):  # Up
            newPos = col + ((row - j) * width)
            if newPos < 0 and j >= 2:
                state, newAdds, unionizer = fillerHelper(state, (col + ((row - 1) * width)), newPos, 0, placed.copy(),
                                                         newAdds, unionizer)
            if newPos < 0:
                break
            if state[newPos] == '-':
                streak += 1
            if j >= 2 and state[newPos] == '#':
                state, newAdds, unionizer = fillerHelper(state, (col + ((row - 1) * width)), newPos, 0, placed.copy(),
                                                         newAdds, unionizer)
            if state[newPos] == '#':
                break
        streak = 0
        for j in range(1, 4):  # Down
            newPos = col + ((row + j) * width)
            if newPos >= height * width and j >= 2:
                state, newAdds, unionizer = fillerHelper(state, (col + ((row + 1) * width)), newPos, 1, placed.copy(),
                                                         newAdds, unionizer)
            if newPos >= height * width:
                break
            if state[newPos] == '-':
                streak += 1
            if j >= 2 and state[newPos] == '#':
                state, newAdds, unionizer = fillerHelper(state, (col + ((row + 1) * width)), newPos, 1, placed.copy(),
                                                         newAdds, unionizer)
            if newPos <= height * width and state[newPos] == '#':
                break
        streak = 0
        for j in range(1, 4):  # Right
            newPos = col + j + (row * width)
            if (col + j >= width or newPos >= height * width) and j >= 2:
                state, newAdds, unionizer = fillerHelper(state, (col + 1 + (row * width)), newPos, 2, placed.copy(),
                                                         newAdds, unionizer)
            if col + j >= width or newPos >= height * width:
                break
            if state[newPos] == '-':
                streak += 1
            if j >= 2 and state[newPos] == '#':
                state, newAdds, unionizer = fillerHelper(state, (col + 1 + (row * width)), newPos, 2, placed.copy(),
                                                         newAdds, unionizer)
            if state[newPos] == '#':
                break
        streak = 0
        for j in range(1, 4):  # Left
            newPos = col - j + (row * width)
            if (col - j < 0 or newPos < 0) and j >= 2:
                state, newAdds, unionizer = fillerHelper(state, (col - 1 + (row * width)), newPos, 3, placed.copy(),
                                                         newAdds, unionizer)
            if col - j < 0 or newPos < 0:
                break
            if state[newPos] == '-':
                streak += 1
            if j >= 2 and state[newPos] == '#':
                state, newAdds, unionizer = fillerHelper(state, (col - 1 + (row * width)), newPos, 3, placed.copy(),
                                                         newAdds, unionizer)
            if state[newPos] == '#':
                break
    placed.update(unionizer)
    return state, placed, newAdds


def backtracking(state, direction, horz, vert, placedLetters, placedBlocks):
    if blockCounter(state) == numBlocking:
        return state
    if blockCounter(state) > numBlocking:
        return None
    var = getNextUnassigned(direction, vert, horz)
    for variable in var:
        iterateOver = getSortedValues(state, variable, direction, placedLetters, placedBlocks)
        for item in iterateOver:
            newState, newPlacedBlocks, pos, oppPos = item
            newHorz, newVert, newPlacedBlocks = fixData(newState, pos, oppPos, horz.copy(), vert.copy(),
                                                        newPlacedBlocks)
            result = backtracking(newState, not direction, newHorz.copy(), newVert.copy(), placedLetters,
                                  newPlacedBlocks.copy())
            if result is not None:
                return result
    return None


def createData(state):
    vertMax = []
    horzMax = []
    for i in range(width):
        x, y, z = fixMaxes(state, True, i)
        vertMax.append((x, y, z))
    for i in range(height):
        x, y, z = fixMaxes(state, False, i)
        horzMax.append((x, y, z))
    return horzMax, vertMax


def printBoard(state):
    printString = ''
    for num, i in enumerate(state):
        if num % width == 0 and num != 0:
            printString += '\n'
        printString += i
        printString += ' '
    print(printString)
    print()


def verifyInput(state, placedBlocks):
    global numBlocking
    if numBlocking == (height * width):
        state = state.replace('-', '#')
        print(state)
        exit()
    toAdd = set()
    for item in placedBlocks:
        col, row = item % width, item // width
        oppPos = (width - col - 1) + ((height - row - 1) * width)
        if state[oppPos] != '#':
            state = state[:oppPos] + '#' + state[oppPos + 1:]
            toAdd.add(oppPos)
    placedBlocks.update(toAdd)
    if height % 2 == 1 and width % 2 == 1 and numBlocking % 2 == 1:
        if (width * height) / 2 not in blocksPlaced and (width * height) / 2 not in wordsPlaced:
            state = state[:int((width * height) / 2)] + '#' + state[int(((width * height) / 2) + 1):]
            blocksPlaced.add(int((width * height) / 2))
    return state, placedBlocks


arguments = ["", "16x16", "184", "twentyk.txt", "V3x2", "H2x3", "H4x4", "V7x4"]
board, wordsPlaced, blocksPlaced = start()
board, blocksPlaced = verifyInput(board, blocksPlaced)
board, blocksPlaced, trash = filler(board, blocksPlaced)
data1, data2 = createData(board)
# printBoard(board)
printBoard(board)
startingtime = time.perf_counter()
answer = backtracking(board, True, data1, data2, wordsPlaced, blocksPlaced)
print(time.perf_counter() - startingtime)

print(answer)
printBoard(answer)
# print()
