import time
import sys

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
    # 'C4': ('#--#-##-#', 3, 2, 2),
    'D1': ('###----##', 3, 2, 1), 'D2': ('--##-##-#', 3, 1, 2), 'D3': ('#####----', 3, 2, 1),
    'D4': ('-##-##--#', 3, 2, 2),
    # 'D4': ('#-##-##--', 3, 2, 2),
    'E1': ('####----#', 3, 2, 1), 'E2': ('-##--##-#', 3, 1, 2),
    'F1': ('###---#-#', 3, 2, 1), 'F2': ('#-#--##-#', 3, 1, 2), 'F3': ('####-#---', 3, 2, 1),
    'F4': ('-##--#-##', 3, 2, 2),
    # 'F4': ('#-##--#-#', 3, 2, 2),
    'G1': ('###--##--', 3, 2, 1), 'G2': ('#-#--#-##', 3, 2, 2)  # 'G2': ('##-#--#-#', 3, 2, 2)
}



def printPiece(key):
    output = ''
    piece, size, ignore, ignore2 = tetrisPieces[key]
    for num, i in enumerate(piece):
        if num != 0 and num % size == 0:
            output += '\n'
        output += i
    print(output)


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
    toAdd = len(toRemove)
    boardBreakdown = [i for j, i in enumerate(boardBreakdown) if j not in toRemove]
    board = ''.join(boardBreakdown)
    for i in range(toAdd):
        board = '          ' + board
    return board


def placeAllPieces(board):
    solutions = []
    heights = [0 for listComp in range(10)]
    removeRows(board)
    for pos, place in enumerate(board):
        if place == '#':
            x, y = pos % 10, pos // 10
            if heights[x] < 20 - y:
                heights[x] = 20 - y
    for colNum in range(10):
        for pieceOrient in tetrisPieces.keys():
            bottomGeo = tetrisPiecesGeo[pieceOrient]
            if len(bottomGeo) + colNum >= 11:
                continue
            rep, size, rightMax, upMax = tetrisPieces[pieceOrient]
            placementHeight = [0 for listComp in range(len(bottomGeo))]
            maxHeight = max(heights[colNum: colNum + len(bottomGeo)])
            if list(bottomGeo).count(0) == len(bottomGeo):
                if maxHeight + upMax >= 20:
                    solutions.append("GAME OVER")
                    continue
                posHeight = maxHeight + size
            else:
                toPass = False
                for colAdd, i in enumerate(bottomGeo):
                    placementHeight[colAdd] = heights[colNum + colAdd] + (upMax - i) + 1
                    if placementHeight[colAdd] > 20:
                        toPass = True
                if toPass:
                    solutions.append("GAME OVER")
                    continue
                posHeight = max(placementHeight) + rep.index('-') // size
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
                    lineCount += 1
            newBoard = removeRows(newBoard)
            solutions.append(newBoard)
    return solutions


# placeAllPieces(
#    "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ############################# ########## #### # # # # ##### ###   ########")
# printBoard(
#    "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
# )
# toPrint = placeAllPieces(
#    "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
# )
toPrint = placeAllPieces(sys.argv[1])
with open("tetrisout.txt", 'w') as f:
    for solutionValues in toPrint:
        f.write("%s\n" % solutionValues)
