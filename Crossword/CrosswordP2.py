import time, sys, copy
import string

height = width = numBlockingSquares = maxDimen = 0
words = []
wordsSub = []
colBreakdown = rowBreakdown = colConstrain = rowConstrain = []
punctuation = set(string.punctuation)


def start():
    sizes = arguments[1]

    global height, width, numBlockingSquares, maxDimen, words, wordsSub
    xPosition = sizes.find('x')
    height = int(sizes[:xPosition])
    width = int(sizes[xPosition + 1:])

    maxDimen = max(width, height)
    words = [set() for x in range(3, maxDimen + 1)]
    wordsSub = [set() for x in range(3, maxDimen + 1)]
    numBlockingSquares = int(arguments[2])
    with open(arguments[3]) as f:
        for line in f:
            line = line.strip()
            line = ''.join(ch for ch in line if ch not in punctuation)
            if line.isalpha() and 3 <= len(line) <= maxDimen:
                words[len(line) - 3].add(line)
                char = ""
                for x in range(len(line) - 1):
                    char += line[x]
                    wordsSub[len(line) - 3].add(char)
    state = ''
    for i in range(height * width):
        state += '-'

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


def isFull(state):
    for item in state:
        if item == '-':
            return False
    return True


def nextToFill(direction, alreadyDoneRow, alreadyDoneCol):
    if direction:
        for i in rowBreakdown:
            for j in i:
                if j not in alreadyDoneRow:
                    return j
    else:
        for i in colBreakdown:
            for j in i:
                if j not in alreadyDoneCol:
                    return j


def getWordLength(spaces, direction):
    num, s, e = spaces
    if direction:
        return e - s + 1
    else:
        return int(((e - s) / width)) + 1


def getPossibleWords(state, wordLength, spaces, position, direction, usedWords):
    num, s, e = spaces
    possibleWords = words[wordLength - 3]
    thisWordRestriction = []
    futureWordRestriction = [[] for x in range(wordLength)]
    if direction:  # Get Constraining Positions
        constraints = rowConstrain[position]
        step = 1
    else:
        constraints = colConstrain[position]
        step = width
    for i in range(s, e + 1, step):  # Constraints in the Words
        if state[i].isalpha():
            if direction:
                thisWordRestriction.append((i - s, state[i]))
            else:
                thisWordRestriction.append((i // width, state[i]))
    for item in constraints:  # Constraints in words branching from this
        if direction:
            firstPosition = item[0]
            futureWordRestriction[firstPosition].append(
                (set(range(s, e + 1)) & set(range(min(item), max(item) + 1, width))).pop())
        else:
            firstPosition = item[0] // width
            futureWordRestriction[firstPosition].append(
                (set(range(s, e + 1, width)) & set(range(min(item), max(item) + 1))).pop())
        for elements in item:
            if state[elements].isalpha():
                futureWordRestriction[firstPosition].append((elements, state[elements]))
        if len(futureWordRestriction[firstPosition]) - 1 == len(item):
            futureWordRestriction[firstPosition].clear()
    positionPossibleWords = {}
    for num, i in enumerate(constraints):  # Different Word Lengths of branching words
        if direction:
            positionPossibleWords[i[0]] = (len(i), words[len(i) - 3])
        else:
            positionPossibleWords[i[0] // width] = (len(i), words[len(i) - 3])

    refinedPossible = []
    for item in possibleWords:
        if item == 'local' and s == 1 and e == 21 and state.find('rotor') != -1:
            print('here')
        if item in usedWords:
            continue
        passer = False
        for restrict in thisWordRestriction:
            index, letter = restrict
            if item[index] != letter:
                passer = True
                break
        if passer: continue
        for wordList, restrict in enumerate(futureWordRestriction):  # Can Be Put Out Because Not Neccesary Every Time
            if len(restrict) == 0: continue
            overlap = restrict[0]
            # places = []
            preWord = ''
            for restrictPerIndex in range(1, len(
                    restrict)):  # When there is a space between letters program dies fix it headasss
                where, letter = restrict[restrictPerIndex]
                if direction:
                    restrictLocation = int(((where - wordList) / width))
                else:
                    restrictLocation = (where - wordList)
                # places.append((restrictLocation, letter))
                preWord += letter
            posOfLetters = [x for x in range(s, e + 1, step)]
            combined = (preWord + item[posOfLetters.index(overlap)])
            if len(combined) != positionPossibleWords[wordList][0]:
                if combined not in wordsSub[positionPossibleWords[wordList][0] - 3]:
                    passer = True
                    break
            elif combined not in positionPossibleWords[wordList][1]:
                passer = True
                break
            if passer: break
        if not passer:
            refinedPossible.append(item)
    return refinedPossible


def placeWords(space, word, state, direction):
    num, s, e = space
    if direction:
        step = 1
    else:
        step = width
    count = 0
    for i in range(s, e + 1, step):
        state = state[:i] + word[count] + state[i + 1:]
        count += 1
    return state


def placingBacktracking(state, direction, usedWords, compRow, compCol):
    if isFull(state):
        return state
    nextSpace = nextToFill(direction, compRow, compCol)  # Fix passing directions
    wordLength = getWordLength(nextSpace, direction)
    posWords = getPossibleWords(state, wordLength, nextSpace, nextSpace[0], direction, usedWords)
    for item in posWords:
        # print(item)
        if item == 'rotor' and nextSpace == (1, 5, 9):
            print('First')
        if item == 'local' and nextSpace == (1, 1, 21):
            print('First')
        newUsedWords = usedWords.copy()
        newUsedWords.add(item)
        newState = placeWords(nextSpace, item, state, direction)
        newCompRow = compRow.copy()
        newCompCol = compCol.copy()
        if direction:
            newCompRow.add(nextSpace)
        else:
            newCompCol.add(nextSpace)
        result = placingBacktracking(newState, not direction, newUsedWords, newCompRow, newCompCol)
        if result is not None:
            return result
    return None


def checkSections(state):
    global rowBreakdown, colBreakdown
    toRemove = set()
    for item in rowBreakdown:
        for i in item:
            num, s, e = i
            breaker = False
            for j in range(s, e + 1):
                if state[j].isalpha() and j == e:
                    breaker = True
                    break
            if breaker:
                toRemove.add(i)
    for item in rowBreakdown:
        for i in toRemove:
            try:
                item.remove(i)
            except ValueError:
                pass
    toRemove = set()
    for item in colBreakdown:
        for i in item:
            num, s, e = i
            breaker = False
            for j in range(s, e + 1, width):
                if state[j].isalpha() and j == e:
                    breaker = True
                    break
            if breaker:
                toRemove.add(i)
    for item in colBreakdown:
        for i in toRemove:
            try:
                item.remove(i)
            except ValueError:
                pass


def sections(state):
    global rowBreakdown, colBreakdown
    rowBreakdown = [[] for x in range(height)]
    colBreakdown = [[] for x in range(width)]
    itemCount = 0
    for i in range(height):
        startIndex = i * width
        for j in range(width):
            position = j + (i * width)
            if (state[position] == '#' or j == width - 1) and startIndex != position:
                rowBreakdown[i].append((itemCount, startIndex, position))
                startIndex = position + 1
                itemCount += 1
    itemCount = 0
    for i in range(width):
        startIndex = i
        for j in range(i, (width * height), width):
            position = j
            if (state[position] == '#' or j // width == height - 1) and startIndex != position:
                colBreakdown[i].append((itemCount, startIndex, position))
                startIndex = position + width
                itemCount += 1
    createConstraints()
    checkSections(state)
    return rowBreakdown, colBreakdown


def createConstraints():
    global colConstrain, rowConstrain
    rowConstrain = [[] for x in range(height)]
    colConstrain = [[] for x in range(width)]
    itemCount = 0
    for item in rowBreakdown:
        for elements in item:
            num, s, e = elements
            for restrict in colBreakdown:
                for restrictElem in restrict:
                    num2, sr, er = restrictElem
                    interHelper = set(range(s, e + 1))
                    if len(interHelper.intersection(range(sr, er + 1))) > 0:
                        toAdd = ()
                        for i in range(sr, er + 1, width):
                            toAdd += (i,)
                        rowConstrain[itemCount].append(toAdd)
        itemCount += 1
    itemCount = 0
    for item in colBreakdown:
        for elements in item:
            num, s, e = elements
            for restrict in rowBreakdown:
                for restrictElem in restrict:
                    num2, sr, er = restrictElem
                    interHelper = set(range(sr, er + 1))
                    if len(interHelper.intersection(range(s, e + 1))) > 0:
                        toAdd = ()
                        for i in range(sr, er + 1):
                            toAdd += (i,)
                        colConstrain[itemCount].append(toAdd)
        itemCount += 1
    print(rowConstrain)
    print(colConstrain)


def printBoard(state):
    printString = ''
    for num, i in enumerate(state):
        if num % width == 0 and num != 0:
            printString += '\n'
        printString += i
        printString += ' '
    print(printString)
    print()


#arguments = ['', '5x5', '0', 'twentyk.txt', 'V0x0price', 'H0x4e']
board, placedList, blocksPlacedList = start()
printBoard(board)
rowSpace, colSpace = sections(board)
print(rowSpace)
print(colSpace)
se = time.perf_counter()
answer = placingBacktracking(board, True, set(), set(), set())
printBoard(answer)
print(time.perf_counter() - se)
