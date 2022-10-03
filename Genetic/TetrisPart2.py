import random
import pickle

NUM_TRIALS = 5
NUM_HEURISTIC = 6
POPULATION_SIZE = 500
NUM_CLONES = 45
TOURNAMENT_SIZE = 30
TOURNAMENT_WIN_PROBABILITY = .75
MUTATION_RATE = .4

pieceClasses = [('A1', 'A2'), ('B1',), ('C1', 'C2', 'C3', 'C4'), ('D1', 'D2', 'D3', 'D4'), ('E1', 'E2'),
                ('F1', 'F2', 'F3', 'F4'), ('G1', 'G2')]

tetrisPiecesGeo = {
    'A1': (0, 0, 0, 0), 'A2': (0,),
    'B1': (0, 0),
    'C1': (1, 1, 0), 'C2': (0, 0), 'C3': (0, 0, 0), 'C4': (0, 2),
    'D1': (0, 1, 1), 'D2': (2, 0), 'D3': (0, 0, 0), 'D4': (0, 0),
    'E1': (0, 0, 1), 'E2': (1, 0), 'E3': (0, 0, 1), 'E4': (1, 0),
    'F1': (1, 0, 1), 'F2': (1, 0), 'F3': (0, 0, 0), 'F4': (0, 1),
    'G1': (1, 0, 0), 'G2': (0, 1), 'G3': (1, 0, 0), 'G4': (0, 1)
}

tetrisPieces = {  # String Rep, Square Size, Maximum Right, Maximum Up
    'A1': ('############----', 4, 3, 0), 'A2': ('-###-###-###-###', 4, 0, 3),
    'B1': ('----', 2, 1, 1),
    'C1': ('###---##-', 3, 2, 1), 'C2': ('#-##-#--#', 3, 1, 2), 'C3': ('###-##---', 3, 2, 1),
    'C4': ('--#-##-##', 3, 2, 2),
    'D1': ('###----##', 3, 2, 1), 'D2': ('--##-##-#', 3, 1, 2), 'D3': ('#####----', 3, 2, 1),
    'D4': ('-##-##--#', 3, 2, 2),
    'E1': ('####----#', 3, 2, 1), 'E2': ('-##--##-#', 3, 1, 2),
    'F1': ('###---#-#', 3, 2, 1), 'F2': ('#-#--##-#', 3, 1, 2), 'F3': ('####-#---', 3, 2, 1),
    'F4': ('-##--#-##', 3, 2, 2),
    'G1': ('###--##--', 3, 2, 1), 'G2': ('#-#--#-##', 3, 2, 2)
}

neighbors = {}


def inBounds(x, y):
    toAllow = [True, True, True, True]  # Up, Down Left Right
    if y == 0:
        toAllow[0] = False
    if y == 19:
        toAllow[1] = False
    if x == 0:
        toAllow[2] = False
    if x == 9:
        toAllow[3] = False
    return toAllow


def createNeighbors():
    for i in range(200):
        posNeighbors = set()
        x, y = i % 10, i // 10
        allowedDirections = inBounds(x, y)
        for direction, element in enumerate(allowedDirections):
            if direction == 0 and element:
                posNeighbors.add(x + ((y - 1) * 10))
            elif direction == 1 and element:
                posNeighbors.add(x + ((y + 1) * 10))
            elif direction == 2 and element:
                posNeighbors.add(x - 1 + (y * 10))
            elif direction == 3 and element:
                posNeighbors.add(x + 1 + (y * 10))
        neighbors[i] = posNeighbors


def printBoard(board):
    output = ''
    for num in range(22):
        if num == 0 or num == 21:
            output += '+'
        else:
            output += '-'
    output += '\n'
    for num, i in enumerate(board):
        if num == 0:
            output += '|'
        if num != 0 and num % 10 == 0:
            output += '|'
            output += '\n'
            output += '|'
        output += i
        output += ' '
    output += '|'
    output += '\n'
    for num in range(22):
        if num == 0 or num == 21:
            output += '|'
        else:
            output += '-'
    output += '\n'
    print(output)


def removeRows(board):
    boardBreakdown = [board[i:i + 10] for i in range(0, len(board), 10)]
    toRemove = []
    for rowNum, rows in enumerate(boardBreakdown):
        toSet = set(rows)
        if len(toSet) == 1 and '#' in toSet:
            toRemove.append(rowNum)
    # toAdd = len(toRemove)
    boardBreakdown = [i for j, i in enumerate(boardBreakdown) if j not in toRemove]
    board = ''.join(boardBreakdown)
    for i in range(len(toRemove)):
        board = '          ' + board
    return board, len(toRemove)


def heightLayout(board):
    heights = [0 for listComp in range(10)]
    for pos, place in enumerate(board):
        if place == '#':
            x, y = pos % 10, pos // 10
            if heights[x] < 20 - y:
                heights[x] = 20 - y
    return heights


def placePiece(board, pieceKey, heights, strategy, spaceLoc, blockLoc):
    solutions = []
    for colNum in range(10):
        strategyPoints = 0
        bottomGeo = tetrisPiecesGeo[pieceKey]
        if len(bottomGeo) + colNum >= 11:
            continue
        rep, size, rightMax, upMax = tetrisPieces[pieceKey]
        placementHeight = [0 for listComp in range(len(bottomGeo))]
        maxHeight = max(heights[colNum: colNum + len(bottomGeo)])
        if list(bottomGeo).count(0) == len(bottomGeo):
            if maxHeight + upMax >= 20:
                # solutions.append("GAME OVER")
                solutions.append((board, strategyPoints, 0,
                                  heuristic(strategy, heights, 0) + -10000, False))
                continue
            posHeight = maxHeight + size
        else:
            toPass = False
            for colAdd, i in enumerate(bottomGeo):
                placementHeight[colAdd] = heights[colNum + colAdd] + (upMax - i) + 1
                if placementHeight[colAdd] > 20:
                    toPass = True
            if toPass:
                # solutions.append("GAME OVER")
                solutions.append((board, strategyPoints, 0,
                                  heuristic(strategy, heights, 0) + -10000, False))
                continue
            posHeight = max(placementHeight) + rep.index('-') // size
        tempSpaceLoc = spaceLoc.copy()
        tempBlockLoc = blockLoc.copy()
        newBoard = board
        spaced = rep.replace('#', ' ')
        posY = posHeight
        lineCount = 0
        for i in spaced:
            if lineCount == size:
                lineCount = 0
                posY -= 1
            poi = colNum + ((20 - posY) * 10) + lineCount
            if poi < 0 or poi > 199:
                lineCount += 1
                continue
            else:
                if i != ' ':
                    newBoard = newBoard[:poi] + '#' + newBoard[poi + 1:]
                    tempSpaceLoc.remove(poi)
                    blockLoc.add(poi)
                lineCount += 1
        newBoard, removedRowsCount = removeRows(newBoard)
        if removedRowsCount == 1:
            strategyPoints += 40
        elif removedRowsCount == 2:
            strategyPoints += 100
        elif removedRowsCount == 3:
            strategyPoints += 300
        elif removedRowsCount == 4:
            strategyPoints += 1200
        tempHeights = heightLayout(newBoard)
        solutions.append(
            (newBoard, strategyPoints, removedRowsCount,
             heuristic(strategy, tempHeights, removedRowsCount),
             True, tempSpaceLoc, tempBlockLoc))
    solutions.sort(reverse=True, key=lambda x: x[3])
    return solutions


def makeNewBoard():
    return ' ' * 200


def holeCount(heights, spaceLoc, blockLoc):
    count = 0
    rowTrans = colTrans = 0
    holeLocations = [False for x in range(10)]
    for loc in spaceLoc:
        col, row = loc % 10, loc // 10
        if heights[col] > 20 - row:
            count += 1
            holeLocations[col] = True
        nextTo = neighbors[loc]
        if loc + 10 in nextTo and loc + 10 in blockLoc:
            colTrans += 1
        if loc - 10 in nextTo and loc - 10 in blockLoc:
            colTrans += 1
        if loc + 1 in nextTo and loc + 1 in blockLoc:
            rowTrans += 1
        if loc - 1 in nextTo and loc - 1 in blockLoc:
            rowTrans += 1
    return count, holeLocations, rowTrans, colTrans


def heightsData(heights):
    totalBump = 0
    maxWell = 0
    totalEmpty = 0
    totalHeight = 0
    for index, i in enumerate(heights):
        totalHeight += i
        if index != 9:
            currWell = abs(i - heights[index + 1])
            maxWell = max(currWell, maxWell)
            totalBump += currWell
        if i == 0:
            totalEmpty += 1
    return totalBump, totalEmpty, maxWell, totalHeight


def heuristic(strategy, heights, linesCleared):
    a, b, c, d, e, f = strategy
    totalBump, totalEmpty, maxWell, heightSum = heightsData(heights)
    value = 0
    value += a * heightSum
    value += b * maxWell
    value += c * totalEmpty
    value += d * totalBump
    value += e * linesCleared
    value += f * max(heights)
    return value


def playGame(strategy):
    board = makeNewBoard()
    spaceLoc = {x for x in range(200)}
    blockLoc = set()
    points = 0
    gameStateOver = False
    moveCount = 0
    while not gameStateOver:
        heightColumnLayout = heightLayout(board)
        pieceChosen = random.choice(pieceClasses)
        maxSolutions = None
        gameOverChecker = [False for x in pieceChosen]
        # print('Move Number %s' % moveCount)
        for iterate, pieces in enumerate(pieceChosen):
            solutions = placePiece(board, pieces, heightColumnLayout, strategy, spaceLoc, blockLoc)
            # printBoard(solutions[0][0])
            # print()
            possGameOver = all(elem[4] is False for elem in solutions)
            if possGameOver:
                gameOverChecker[iterate] = True
            if maxSolutions is None or maxSolutions[3] < solutions[0][3]:
                maxSolutions = solutions[0]
        if all(gameOverChecker):
            gameStateOver = True
        else:
            board = maxSolutions[0]
            points += maxSolutions[1]
            # print('Current Points: %s' % points)
        moveCount += 1
    return points


def playGame2(strategy):
    board = makeNewBoard()
    spaceLoc = {x for x in range(200)}
    blockLoc = set()
    points = 0
    gameStateOver = False
    moveCount = 0
    while not gameStateOver:
        heightColumnLayout = heightLayout(board)
        pieceChosen = random.choice(pieceClasses)
        maxSolutions = None
        gameOverChecker = [False for x in pieceChosen]
        # print('Move Number %s' % moveCount)
        for iterate, pieces in enumerate(pieceChosen):
            solutions = placePiece(board, pieces, heightColumnLayout, strategy, spaceLoc, blockLoc)
            # printBoard(solutions[0][0])
            # print()
            possGameOver = all(elem[4] is False for elem in solutions)
            if possGameOver:
                gameOverChecker[iterate] = True
            if maxSolutions is None or maxSolutions[3] < solutions[0][3]:
                maxSolutions = solutions[0]
        if all(gameOverChecker):
            gameStateOver = True
        else:
            board = maxSolutions[0]
            points += maxSolutions[1]
            printBoard(board)
            print("Current score: %s" % points)
        moveCount += 1


def fitnessFunction(strategy, stratNumber):
    gameScores = []
    print("Evaluating strategy number %s -->" % stratNumber, end=" ")
    for count in range(NUM_TRIALS):
        gameScores.append(playGame(strategy))
    avg = sum(gameScores) / len(gameScores)
    print(avg)
    return avg


def breed(parent1, parent2):
    main, nonMain = (parent1[0], parent2[0]) if random.random() < .5 else (parent2[0], parent1[0])
    copyPos = random.randint(1, NUM_HEURISTIC)
    child = main[0:copyPos] + nonMain[copyPos:NUM_HEURISTIC]
    if random.random() < MUTATION_RATE:
        child = list(child)
        child[random.randint(0, len(parent1) - 1)] += random.uniform(-1, 1)
        return tuple(child)
    return child


def genetic():
    userIDecision = input("(N)ew process, or (L)oad saved process? ")
    sStrategy = []
    skipper = False
    initial = 0
    if userIDecision == 'N':
        while len(sStrategy) < POPULATION_SIZE:
            sStrategy.append(tuple(random.uniform(-1, 1) for i in range(NUM_HEURISTIC)))
    elif userIDecision == 'L':
        filename = input("What filename? ")
        with open(filename, 'rb') as handle:
            loadedData = pickle.load(handle)
        initial = loadedData[1]
        print("Generation: %s" % loadedData[1])
        print('Best Strategy so far: %s with score of %s' % (loadedData[0][0][0], loadedData[0][0][1]))
        sStrategy = loadedData[0]
        skipper = True
    for iterate in range(initial, 10000):
        if not skipper:
            # Fitness Function on Strats
            sStrategy = [(x, fitnessFunction(x, number)) for number, x in enumerate(sStrategy)]
            sStrategy.sort(reverse=True, key=lambda x: x[1])
            print('Best Strategy so far: %s with score of %s' % (sStrategy[0][0], sStrategy[0][1]))
            print('Average: %s' % (sum([x[1] for x in sStrategy]) / len(sStrategy)))
        while True:
            skipper = False
            userDecision = input("(P)lay a game with current best strategy, (S)ave current process, or (C)ontinue? ")
            if userDecision == 'C':
                # New Generation
                nextGen = [sStrategy[x][0] for x in range(0, NUM_CLONES)]
                prevCreated = set(nextGen)
                # Tourney
                tourneyParticipants = random.sample(sStrategy, 2 * TOURNAMENT_SIZE)
                tourney1 = sorted(tourneyParticipants[:len(tourneyParticipants) // 2], key=lambda x: x[1], reverse=True)
                tourney2 = sorted(tourneyParticipants[len(tourneyParticipants) // 2:], key=lambda x: x[1], reverse=True)
                # Breeding
                parent1 = parent2 = None
                while len(nextGen) < POPULATION_SIZE:
                    for i in tourney1:
                        if random.random() < TOURNAMENT_WIN_PROBABILITY:
                            parent1 = i
                            break
                    for i in tourney2:
                        if random.random() < TOURNAMENT_WIN_PROBABILITY:
                            parent2 = i
                            break
                    child = breed(parent1, parent2)
                    if child not in prevCreated:
                        nextGen.append(child)
                        prevCreated.add(child)
                sStrategy = nextGen.copy()
                break
            elif userDecision == 'P':
                playGame2(sStrategy[0][0])
            elif userDecision == 'S':
                filename = input("What filename? ")
                with open(filename, 'wb') as handle:
                    #pickle.dump((sStrategy, iterate), handle, protocol=pickle.HIGHEST_PROTOCOL)
                    pickle.dump((sStrategy, iterate), handle)
                exit()


createNeighbors()
genetic()
