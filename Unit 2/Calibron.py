import sys
import copy
import time


def getSortedValues(var, spots):
    potential = []
    for s, boolean in enumerate(spots):
        if not boolean:
            leftColumn, leftRow = s % puzzle_width, s // puzzle_width
            height, width = var
            breaker = False
            for i in range(leftRow, (leftRow + height)):
                for j in range(leftColumn, (leftColumn + width)):
                    pos = (i * puzzle_width) + j
                    if i >= puzzle_height or j >= puzzle_width or spots[pos] is True:
                        breaker = True
                        break
                if breaker:
                    break
            if not breaker:
                potential.append((leftColumn, leftRow))
    return potential


def spotFixer(rect, spots):
    leftRow, leftColumn, height, width = rect
    for i in range(leftRow, leftRow + height):
        for j in range(leftColumn, leftColumn + width):
            pos = (i * puzzle_width) + j
            spots[pos] = True
    return spots


def backtracking(state, remaining, spots):
    if len(remaining) == 0:
        return state
    # reversedVar = reversed(remaining[len(remaining) - 1])
    var = [remaining[len(remaining) - 1], remaining[len(remaining) - 1][::-1]]
    if var[0] == var[1]:
        var.pop()
    newRemaining = remaining.copy()
    newRemaining.pop()
    for variables in var:
        for valX, valY in getSortedValues(variables, spots):
            newSpots = spots.copy()
            newState = state.copy()
            newState.append((valY, valX, variables[0], variables[1]))
            newSpots = spotFixer(newState[len(newState) - 1], newSpots.copy())
            result = backtracking(newState, newRemaining, newSpots.copy())
            if result is not None:
                return result
    return None


# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
# puzzle = sys.argv[1].split()
puzzle = input()
puzzle = puzzle.split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions

totalArea = 0
for x, y in rectangles:
    totalArea += (x * y)
if totalArea != (puzzle_height * puzzle_width):
    print("Containing rectangle incorrectly sized.")
    exit()
availableSpots = [False for x in range(puzzle_height * puzzle_width)]
start = time.perf_counter()
answer = backtracking([], rectangles.copy(), availableSpots)
print(answer)
end = time.perf_counter()
print(end - start)
# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
#
# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.
