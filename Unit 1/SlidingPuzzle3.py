from time import perf_counter
from collections import deque
import heapq
import sys
import copy
import random

loc = {'A': (0, 0), 'B': (1, 0), 'C': (2, 0), 'D': (3, 0),
       'E': (0, 1), 'F': (1, 1), 'G': (2, 1), 'H': (3, 1),
       'I': (0, 2), 'J': (1, 2), 'K': (2, 2), 'L': (3, 2),
       'M': (0, 3), 'N': (1, 3), 'O': (2, 3)}


def taxicab(board):
    count = 0
    size = len(board) ** 0.5
    goal = find_goal(board)
    for val in board:
        if val != '.':
            x, y = oneTotwo(board.find(val), size)
            xg, yg = oneTotwo(goal.find(val), size)
            count += abs(yg - y) + abs(xg - x)
    return count


def inversionCount(board):
    count = 0
    board = board.replace(".", "")
    copy = board
    for x in board[1:]:
        while copy[int(copy.find(x) - 1)] > x and int(copy.find(x)) - 1 >= 0:
            switch = list(copy)
            hold = switch.index(x)
            temp = switch[hold - 1]
            switch[hold] = temp
            switch[hold - 1] = x
            copy = "".join(switch)
            count += 1
    if count != 0:
        mx = 0
    return count


def rcCount(col, rowNum, char, state):
    total = 0
    total2 = 0
    conflicts = []
    conflicts2 = []
    goalc, goalr = loc[char]
    for i in range(4):
        spot = i + rowNum * 4
        spot2 = col + i * 4
        if state[spot] != '.' and i != col:
            goalTc, goalTr = loc[state[spot]]
            if i < col:
                if goalTc > goalc and goalTr == goalr and goalr == rowNum:
                    conflicts.append(spot % 4)
                    total += 1
            else:
                if goalTc < goalc and goalTr == goalr and goalr == rowNum:
                    conflicts.append(spot % 4)
                    total += 1
        if state[spot2] != '.' and i != rowNum:
            goalTc, goalTr = loc[state[spot2]]
            if i < rowNum:
                if goalTr > goalr and goalTc == goalc and goalc == col:
                    conflicts2.append(spot2 // 4)
                    total2 += 1
            else:
                if goalTr < goalr and goalTc == goalc and goalc == col:
                    conflicts2.append(spot2 // 4)
                    total2 += 1
    rValue = (total, conflicts, total2, conflicts2)
    return rValue


def linearC(state):
    total = 0
    colSaves = []
    conflictPos = []
    for i in range(4):
        tileConflict = []
        for j in range(4):
            spot = j + (i * 4)
            if state[spot] != '.':
                val, conflicts, val2, conflicts2 = rcCount(j, i, state[spot], state)
                tileConflict.append([val, conflicts])
                colSaves.append([val2, conflicts2])
            else:
                tileConflict.append([0, []])
                colSaves.append([0, []])
        val = max(tileConflict)
        while val[0] != 0:
            conflictPos.append((i, True))
            pos = tileConflict.index(val)
            for y in tileConflict[pos][1]:
                tileConflict[y][0] -= 1
                tileConflict[y][1].remove(pos)
            val[0], val[1] = 0, []
            total += 1
            val = max(tileConflict)
    for i in range(4):
        temp = colSaves[i::4]
        val = max(temp)
        while val[0] != 0:
            conflictPos.append((i, False))
            val = max(temp)
            pos = temp.index(val)
            for y in temp[pos][1]:
                temp[y][0] -= 1
                temp[y][1].remove(pos)
            val[0], val[1] = 0, []
            total += 1
    final = total * 2
    return final, conflictPos


def linearC2(state, conflicts, newSpotx, newSpoty, oldSpotx, oldSpoty, old, direction):
    returnValue = old
    total = 0
    rowC = colC = False
    if len(conflicts) > 1:
        mx = 0
    conflictPos = list(dict.fromkeys(conflicts))
    if direction:
        for i in conflictPos:
            pos, row = i
            if not row and oldSpotx == pos:
                colC = True
                conflictPos.remove(i)
                returnValue -= 2
            if not row and newSpotx == pos:
                conflictPos.remove(i)
                returnValue -= 2
        spot = newSpotx + (newSpoty * 4)
        g1, g2, val, conflicts = rcCount(newSpotx, newSpoty, state[spot], state)
        if val != 0 or colC:
            colSaves = []
            colOld = []
            for i in range(4):
                g1, g2, val, conflicts = rcCount(newSpotx, i, state[newSpotx + (i * 4)], state)
                colSaves.append([val, conflicts])
                if colC:
                    spot = oldSpotx + (i * 4)
                    if state[spot] != '.':
                        g1, g2, val, conflicts = rcCount(oldSpotx, i, state[oldSpotx + (i * 4)], state)
                        colOld.append([val, conflicts])
                    else:
                        colOld.append([0, []])
            val = max(colSaves)
            while val[0] != 0:
                conflictPos.append((newSpotx, False))
                val = max(colSaves)
                pos = colSaves.index(val)
                for y in colSaves[pos][1]:
                    colSaves[y][0] -= 1
                    colSaves[y][1].remove(pos)
                val[0], val[1] = 0, []
                total += 1
            if colC:
                val = max(colOld)
                while val[0] != 0:
                    conflictPos.append((newSpotx, False))
                    val = max(colSaves)
                    pos = colSaves.index(val)
                    for y in colSaves[pos][1]:
                        colSaves[y][0] -= 1
                        colSaves[y][1].remove(pos)
                    val[0], val[1] = 0, []
                    total += 1
    else:
        for i in conflictPos:
            pos, row = i
            if row and oldSpoty == pos:
                rowC = True
                conflictPos.remove(i)
                returnValue -= 2
            if row and newSpoty == pos:
                conflictPos.remove(i)
                returnValue -= 2
        spot = newSpotx + (newSpoty * 4)
        val, conflicts, g1, g2 = rcCount(newSpotx, newSpoty, state[spot], state)
        if val != 0 or rowC:
            rowSaves = []
            rowOld = []
            for i in range(4):
                val, conflicts, g1, g2 = rcCount(i, newSpoty, state[i + (newSpoty * 4)], state)
                rowSaves.append([val, conflicts])
                if rowC:
                    spot = i + (oldSpoty * 4)
                    if state[spot] != '.':
                        val, conflicts, g1, g2 = rcCount(i, oldSpoty, state[i + (oldSpoty * 4)], state)
                        rowOld.append([val, conflicts])
                    else:
                        rowOld.append([0, []])
            val = max(rowSaves)
            while val[0] != 0:
                conflictPos.append((newSpoty, True))
                val = max(rowSaves)
                pos = rowSaves.index(val)
                for y in rowSaves[pos][1]:
                    rowSaves[y][0] -= 1
                    rowSaves[y][1].remove(pos)
                val[0], val[1] = 0, []
                total += 1
            if rowC:
                val = max(rowOld)
                while val[0] != 0:
                    conflictPos.append((newSpoty, False))
                    val = max(rowOld)
                    pos = rowOld.index(val)
                    for y in rowOld[pos][1]:
                        rowOld[y][0] -= 1
                        rowOld[y][1].remove(pos)
                    val[0], val[1] = 0, []
                    total += 1
    returnValue += total * 2
    return returnValue, conflictPos


def taxicab2(char, indexOx, indexOy, indexNx, indexNy, old):
    posGx, posGy = loc[char]
    if abs(posGx - indexOx) + abs(posGy - indexOy) > abs(posGx - indexNx) + abs(posGy - indexNy):
        return old - 1
    else:
        return old + 1


def parityCheck(board):
    start = perf_counter()
    size = len(board) ** 0.5
    even = size % 2 == 0
    count = inversionCount(board)
    if even:
        x, y = oneTotwo(board.find("."), size)
        if count % 2 == 0:
            if (size - y) % 2 == 0:
                end = perf_counter()
                return False, end - start
        else:
            if (size - y) % 2 == 1:
                end = perf_counter()
                return False, end - start
    else:
        if count % 2 == 1:
            end = perf_counter()
            return False, end - start
    end = perf_counter()
    return True, None


def print_puzzle(board, size):
    output = ''
    for i in range(len(board)):
        if i % size == 0 and i > 0:
            output += "\n"
        output += board[i] + " "
    print(output + "\n")


def find_goal(board):
    board = sorted(board)
    board.append(board.pop(0))
    return "".join(board)
    # return "ABCDEFGHIJKLMNO."
    # return "ABCDEFGHIJKLMNO."


def goal_test(test):
    if test == find_goal(test):
        return True
    return False


def swap(list, pos, posSwap):
    list[pos], list[posSwap] = list[posSwap], list[pos]
    return "".join(list)


def twoToOne(x, y, size):
    return x + (y * size)


def oneTotwo(index, size):
    return index % size, index // size


def get_children(parent):
    children = []
    size = int(len(parent) ** (1 / 2))
    pos = parent.find(".")
    posx, posy = pos % 4, pos // 4
    if posx + 1 <= size - 1:
        children.append(
            (swap(list(parent), pos, posx + 1 + (posy * 4)), posx + 1, posy, posx, posy, True))
    if posx - 1 >= 0:
        children.append(
            (swap(list(parent), pos, posx - 1 + (posy * 4)), posx - 1, posy, posx, posy, True))
    if posy + 1 <= size - 1:
        children.append(
            (swap(list(parent), pos, posx + (posy + 1) * 4), posx, posy + 1, posx, posy, False))
    if posy - 1 >= 0:
        children.append(
            (swap(list(parent), pos, posx + (posy - 1) * 4), posx, posy - 1, posx, posy, False))
    return children


def astar(start):
    s = perf_counter()
    closed = {""}
    conflicts, spots = linearC(start)
    data = (taxicab(start) + conflicts, start, 0, taxicab(start), conflicts, spots)
    fringe = []
    heapq.heappush(fringe, data)
    while len(fringe) != 0:
        heuristic, state, depth, trueHeuristic, saves, where = heapq.heappop(fringe)
        if goal_test(state):
            e = perf_counter()
            return depth, (e - s)
        if state not in closed:
            closed.add(state)
            listChildren = get_children(state)
            #random.shuffle(listChildren)
            for child in listChildren:
                new_state, posOx, posOy, posNx, posNy, direction = child
                if new_state not in closed:
                    t2 = taxicab2(state[posOx + (posOy * 4)], posOx, posOy, posNx, posNy, trueHeuristic)
                    val, place = linearC2(new_state, where, posNx, posNy, posOx, posOy, saves, direction)
                    new_data = (depth + 1 + t2 + val, new_state, depth + 1, t2, val, place)
                    heapq.heappush(fringe, new_data)
    return None, None


with open(sys.argv[1]) as f:
    s = perf_counter()
    i = 0
    for line in f:
        if parityCheck(line.strip()):
            moves, time = astar(line.strip())
            print("Line %s: %s, A* - %s moves in %s seconds" % (i, line.strip(), moves, time))
        i += 1
    e = perf_counter()
    print("Time = %s" % (e - s))
