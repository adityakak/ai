import sys


def value(character):
    if character == 'O':
        return -1
    if character == 'X':
        return 1


def gameOver(board):
    if (board[0] == board[1] == board[2]) and board[0] != '.':
        return value(board[0])
    if (board[3] == board[4] == board[5]) and board[3] != '.':
        return value(board[3])
    if (board[6] == board[7] == board[8]) and board[6] != '.':
        return value(board[6])
    if (board[0] == board[3] == board[6]) and board[0] != '.':
        return value(board[0])
    if (board[1] == board[4] == board[7]) and board[1] != '.':
        return value(board[1])
    if (board[2] == board[5] == board[8]) and board[2] != '.':
        return value(board[2])
    if (board[0] == board[4] == board[8]) and board[0] != '.':
        return value(board[0])
    if (board[2] == board[4] == board[6]) and board[2] != '.':
        return value(board[2])
    for i in board:
        if i == '.':
            return float('inf')
    return 0


def dotPos(board):
    return [i for i in range(len(board)) if board[i] == '.']


def possibleNextBoard(board, player):
    possible = []
    insert = player
    for i in dotPos(board):
        new_string = board[:i] + str(insert) + board[i + 1:]
        possible.append(new_string)
    return possible


def possibleNextBoard2(board, player):
    possible = []
    insert = player
    for i in dotPos(board):
        new_string = board[:i] + str(insert) + board[i + 1:]
        possible.append((new_string, i))
    return possible


def printBoard(board):
    output = ''
    row = 0
    for num in range(len(board)):
        if num != 0 and num % 3 == 0:
            output += '\n'
            row += 1
        output += board[num] + ' '
    print(output)


def minStep(board):
    if gameOver(board) != float('inf'):
        return gameOver(board)
    results = list()
    for nextBoard in possibleNextBoard(board, 'O'):
        results.append(maxStep(nextBoard))
    return min(results)


def maxStep(board):
    if gameOver(board) != float('inf'):
        return gameOver(board)
    results = list()
    for nextBoard in possibleNextBoard(board, 'X'):
        results.append(minStep(nextBoard))
    return max(results)


def maxMove(board):
    if gameOver(board) != float('inf'):
        return gameOver(board)
    results = list()
    resultsPos = list()
    dictionary = {}
    possibles = possibleNextBoard2(board, 'X')
    for nextBoard, position in possibles:
        results.append(minStep(nextBoard))
        resultsPos.append(position)
        dictionary[position] = nextBoard
        if results[len(results) - 1] == 0:
            status = 'tie'
        elif results[len(results) - 1] == 1:
            status = 'win'
        else:
            status = 'loss'
        print("Moving at", position, "results in a %s" % status)
    number = max(results)
    number2 = results.index(number)
    number3 = resultsPos[number2]
    print()
    print("I choose space %s" % number3)
    print()
    return dictionary[number3]


def minMove(board):
    if gameOver(board) != float('inf'):
        return gameOver(board)
    results = list()
    resultsPos = list()
    dictionary = {}
    for nextBoard, position in possibleNextBoard2(board, 'O'):
        results.append(maxStep(nextBoard))
        resultsPos.append(position)
        dictionary[position] = nextBoard
        if results[len(results) - 1] == 0:
            status = 'tie'
        elif results[len(results) - 1] == 1:
            status = 'loss'
        else:
            status = 'win'
        print("Moving at", position, "results in a %s" % status)
    number = min(results)
    number2 = results.index(number)
    number3 = resultsPos[number2]
    print()
    print("I choose space %s" % number3)
    print()
    return dictionary[number3]


def printCurrentBoard(board):
    print("Current board:")
    output = ''
    row = 0
    for num in range(len(board)):
        if num != 0 and num % 3 == 0:
            if num == 3:
                output += '\t012'
            elif num == 6:
                output += '\t345'
            output += '\n'
            row += 1
        output += board[num]
    output += '\t678'
    print(output)


def availableSpots(board):
    spots = []
    for values in range(len(board)):
        if board[values] == '.':
            spots.append(values)
    print("You can move to any of these spaces:", spots)


print("Input Starting Board State:")
#initialBoard = sys.argv[1]
initialBoard = '.........'
print()
printCurrentBoard(initialBoard)
print()
turn = True
if gameOver(initialBoard) != float('inf'):
    print("No one should move the game is already over")
elif initialBoard.find("O") == -1 and initialBoard.find("X") == -1:
    print("Should the Computer go first? (Y/N)")
    whoseTurn = input()
    if whoseTurn != 'Y':
        turn = False
    print()
computerToken = ""
xCount = oCount = 0
for x in initialBoard:
    if x == 'X':
        xCount += 1
    if x == 'O':
        oCount += 1
if xCount == oCount:
    if turn:
        computerToken = 'X'
    else:
        computerToken = 'O'
else:
    if turn:
        computerToken = 'O'
    else:
        computerToken = 'X'
while gameOver(initialBoard) == float('inf'):
    if turn:
        if computerToken == 'X':
            initialBoard = maxMove(initialBoard)
        else:
            initialBoard = minMove(initialBoard)
        turn = not turn
        printCurrentBoard(initialBoard)
        print()
    else:
        availableSpots(initialBoard)
        print("Your choice?")
        playerMove = int(input())
        print()
        if computerToken == 'X':
            initialBoard = initialBoard[:playerMove] + 'O' + initialBoard[playerMove + 1:]
        else:
            initialBoard = initialBoard[:playerMove] + 'X' + initialBoard[playerMove + 1:]
        turn = not turn
        printCurrentBoard(initialBoard)
        print()
score = gameOver(initialBoard)
if score == 0:
    print("We tied!")
elif score == 1 and computerToken == 'X':
    print("I Win!")
elif score == 1 and computerToken == 'O':
    print("You Win!")
elif score == -1 and computerToken == 'O':
    print("I Win!")
elif score == -1 and computerToken == 'X':
    print("You Win!")
