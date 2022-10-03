import sys


def value2(character, player):
    if player == 'O':  # Different Score depending on who the player is, basically sign flip
        if character == 'O':
            return 1
        if character == 'X':
            return -1
    else:
        if character == 'O':
            return -1
        if character == 'X':
            return 1


def gameOver2(board, player):
    if (board[0] == board[1] == board[2]) and board[0] != '.':  # Checks all the board combinations to see if
        return value2(board[0], player)  # a three in a row has been established
    if (board[3] == board[4] == board[5]) and board[3] != '.':
        return value2(board[3], player)
    if (board[6] == board[7] == board[8]) and board[6] != '.':
        return value2(board[6], player)
    if (board[0] == board[3] == board[6]) and board[0] != '.':
        return value2(board[0], player)
    if (board[1] == board[4] == board[7]) and board[1] != '.':
        return value2(board[1], player)
    if (board[2] == board[5] == board[8]) and board[2] != '.':
        return value2(board[2], player)
    if (board[0] == board[4] == board[8]) and board[0] != '.':
        return value2(board[0], player)
    if (board[2] == board[4] == board[6]) and board[2] != '.':
        return value2(board[2], player)
    for i in board:  # If the board is not completely filled return infinity otherwise return 0 to indicate a draw
        # position
        if i == '.':
            return float('inf')
    return 0


def value(character):
    if character == 'O':
        return -1
    if character == 'X':
        return 1


def gameOver(board):  # Checks game irrespective of player
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
    return [i for i in range(len(board)) if board[i] == '.']  # Returns all available spots


def possibleNextBoard(board, player):  # Iterates through all available positions and inserts
    possible = []  # the respective players character
    insert = player
    for i in dotPos(board):
        new_string = board[:i] + str(insert) + board[i + 1:]
        possible.append(new_string)
    return possible


def possibleNextBoard2(board, player):  # Same as the preceding one but also returns position of spot for telemetry
    possible = []
    insert = player
    for i in dotPos(board):
        new_string = board[:i] + str(insert) + board[i + 1:]
        possible.append((new_string, i))
    return possible


def negaMaxStep(board, player):
    if gameOver2(board, player) != float(
            'inf'):  # Checks to see if the board is complete or not and returns score if it is
        return gameOver2(board, player)
    if player == 'O':  # Flips the token for the next negaMaxStep Call
        token = 'X'
    else:
        token = 'O'
    results = list()  # Creates a list to hold result values i.e (0, -1, 1)
    for nextBoard in possibleNextBoard(board,
                                       player):  # Creates new board states and calls negaMax on it using the other
        # players "perspective"
        values = negaMaxStep(nextBoard, token)
        results.append(-1 * values)
    return max(results)


def negaMaxMove(board, player):
    if gameOver2(board, player) != float('inf'):  # Checks to see if the board is complete or not and returns score if
        # it is
        return gameOver2(board, player)
    results = list()
    resultsPos = list()  # Holds the position the character was added in for telemetry
    dictionary = {}  # Holds a reference between the position the character was changed in too the board state
    possibles = possibleNextBoard2(board, player)
    if player == 'O':
        token = 'X'
    else:
        token = 'O'
    for nextBoard, position in possibles:  # Provides Position as well as board state for telemetry
        values = negaMaxStep(nextBoard, token)
        results.append(-1 * values)
        resultsPos.append(position)
        dictionary[position] = nextBoard
        if results[len(results) - 1] == 0:  # Prints out telemetry values for each spot
            status = 'tie'
        elif results[len(results) - 1] == -1:
            status = 'loss'
        else:
            status = 'win'
        print("Moving at", position, "results in a %s" % status)
    number = max(results)  # Finds the max value of the negaMax
    number2 = results.index(
        number)  # Finds the index of the result to find its position on the board in the next statement
    number3 = resultsPos[number2]
    print()
    print("I choose space %s" % number3)  # Prints out position being chosen
    print()
    return dictionary[number3]  # Return the board state based on the chosen position


def printCurrentBoard(board):  # Prints out the current board as long as a numerical guide
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


def availableSpots(board):  # Prints user telemetry on what spots they can choose
    spots = []
    for values in range(len(board)):
        if board[values] == '.':
            spots.append(values)
    print("You can move to any of these spaces:", spots)


print("Input Starting Board State:")
initialBoard = sys.argv[1]
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
        initialBoard = negaMaxMove(initialBoard, computerToken)
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
