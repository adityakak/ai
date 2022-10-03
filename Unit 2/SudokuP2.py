import time, copy, sys

N = subH = subW = None
symbolSet = []
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
dictBoard = {}
symbolCount = {}
constraints = {}
constrainGroups = []
edges = []


def factor(num):
    factoring = []
    for j in range(1, num + 1):
        if num % j == 0:
            factoring.append(j)
    return factoring


def printBoard(state):
    output = ''
    row = 0
    for num in range(len(state)):
        if num != 0 and num % N == 0:
            output += '\n'
            row += 1
        output += state[num] + ' '
    print(output)


def getNextUnassigned(possible):
    minimum = float('inf')
    minPos = 0
    for num, val in enumerate(possible):
        if minimum > len(val) > 1:
            minPos = num
            minimum = len(val)
    return minPos


def getSortedValues(var, possible):
    string = possible[var]
    returnVals = []
    for vals in string:
        returnVals.append(vals)
    return returnVals


def backtracking(state, possible):
    if state.find('.') == -1:
        return state
    var = getNextUnassigned(possible)
    for val in getSortedValues(var, possible):
        newState = state[:var] + str(val) + state[var + 1:]
        possible[var] = str(val)
        newPossible = possible.copy()
        checkedBoard, newPossible = constraintProp(newState, newPossible, var)
        if checkedBoard is not None:
            result = backtracking(checkedBoard, newPossible)
            if result is not None:
                return result
    return None


def findEdge(index):
    x, y = index % N, index // N
    xSpot, ySpot = x // subW, y // subH
    return xSpot * subW, ySpot * subH


def saveRemove(sets, removed):
    try:
        if len(sets) != 0:
            sets.remove(removed)
            return sets
    except KeyError:
        return sets


def cleaner(board, val, cons, possible):
    newSpots = []
    done = set()
    for iterate in range(3):
        for y in cons[iterate]:
            #if board[y] == "." and y not in done:
            if y not in done:
                done.add(y)
                if val in possible[y]:
                    possible[y] = possible[y].replace(val, '')
                if len(possible[y]) == 1 and board[y] == ".":
                    board = board[:y] + possible[y] + board[y + 1:]
                    newSpots.append(y)
                elif len(possible[y]) == 0:
                    return None, [], []
    return board, possible, newSpots


def forwardLooking(board, possible):
    spots = []
    solved = []
    for num, z in enumerate(board):
        if z != ".":
            spots.append(num)
    while len(spots) != 0:
        z = spots[0]
        if board.find(".") == -1:
            break
        val = board[z]
        cons = constraints[z]
        board, possible, news = cleaner(board, val, cons, possible)
        if board is None: return None, None
        for iterate in news:
            if iterate not in solved:
                spots.append(iterate)
        solved += news
        spots.pop(0)
    return board, possible


def forwardLooking2(board, possible, given):
    solved = []
    spots = given
    while len(spots) != 0:
        z = spots[0]
        if board.find(".") == -1:
            break
        val = board[z]
        cons = constraints[z]
        board, possible, news = cleaner(board, val, cons, possible.copy())
        if board is None: return None, None
        for iterate in news:
            if iterate not in solved:
                spots.append(iterate)
        solved += news
        spots.pop(0)
    return board, possible


def debugHelper(group, possible):
    returnVals = []
    for val in group:
        returnVals.append(possible[val])
    return returnVals


def constrainChecker(board, possible, group):
    solved = []
    someSymbols = symbolSet.copy()
    for val in group:
        if board[val] != ".":
            if possible[val] in someSymbols:
                someSymbols.remove(possible[val])
    for val in someSymbols:
        has = []
        solvedWValue = []
        for values in group:
            if len(possible[values]) == 1 and val in possible[values]:
                solvedWValue.append(values)
            if val in possible[values] and board.find(".") != -1:
                has.append(values)
            if len(has) >= 2:
                break
        if len(has) == 0 and len(solvedWValue) == 0:
            return None, None, None
        elif len(has) == 1 and len(solvedWValue) == 0:
            possible[has[0]] = val
            board = board[:has[0]] + str(val) + board[has[0] + 1:]
            solved.append(has[0])
    return board, possible, solved


def constraintProp(board, possible, inputted):
    if inputted is not None:
        board, possible = forwardLooking2(board, possible, [inputted])
    if board is None:
        return None, None
    while True:
        totalSolved = []
        for constrains in constrainGroups:
            if board.find('.') == -1:
                return board, possible
            board, possible, solved = constrainChecker(board, possible.copy(), constrains)
            if board is None:
                return None, None
            totalSolved += solved
        temps = copy.copy(board)
        if len(totalSolved) != 0:
            board, possible = forwardLooking2(board, possible.copy(), totalSolved)
            '''
            if board == temps:
                possible = newPossible
                break
            '''
            if board is not None and temps == board:
                break
            elif board is None:
                return None, None
        else:
            break
    return board, possible


def debugHelper2(possibilites):
    canidates = []
    for x in possibilites:
        if len(x) > 1:
            canidates.append(x)
    return canidates


def solutionChecker(board):
    for x in constrainGroups:
        checker = symbolSet.copy()
        for indices in x:
            try:
                checker.remove(board[indices])
            except ValueError:
                input()
        if len(checker) > 0:
            input()


start = time.perf_counter()
with open("sudoku_puzzles_1.txt") as f:
    i = 1
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
        puzzlePossible = []
        for number in range(len(puzzle)):
            edgeX, edgeY = findEdge(number)
            edgeLocation = edgeX + (edgeY * N)
            if edgeLocation not in edges:
                edges.append(edgeLocation)
            if puzzle[number] == '.':
                puzzlePossible.append("".join(symbolSet))
            else:
                puzzlePossible.append(puzzle[number])
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
        edges = sorted(edges)
        for x in range(N):
            temp = (constraints[edges[x]][2]).copy()
            temp.add(edges[x])
            constrainGroups.append(temp)
        for x in range(N):
            temp = (constraints[x][1]).copy()
            temp.add(x)
            constrainGroups.append(temp)
        for x in range(N):
            temp = (constraints[x * N][0]).copy()
            temp.add(x * N)
            constrainGroups.append(temp)
        puzzle, puzzlePossible = forwardLooking(puzzle, puzzlePossible)
        puzzle, puzzlePossible = constraintProp(puzzle, puzzlePossible, None)
        answer = backtracking(puzzle, puzzlePossible)
        #solutionChecker(answer)
        constrainGroups.clear()
        #print(i, answer)
        print(answer)
        end = time.perf_counter()
        print(end - start)
        i += 1

