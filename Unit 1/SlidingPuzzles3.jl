#using DataStructures: AbstractHeap
using DataStructures
using Printf
using Random


loc = Dict(
    'A' => (0, 0),
    'B' => (1, 0),
    'C' => (2, 0),
    'D' => (3, 0),
    'E' => (0, 1),
    'F' => (1, 1),
    'G' => (2, 1),
    'H' => (3, 1),
    'I' => (0, 2),
    'J' => (1, 2),
    'K' => (2, 2),
    'L' => (3, 2),
    'M' => (0, 3),
    'N' => (1, 3),
    'O' => (2, 3),
)

#println("\nTypedDictionary = ", loc)

function print_puzzle(board, boardSize)
    output = ' '
    for i = 0:length(board)
        if mod(i, boardSize) == 0 & i > 0
            output *= "\n"
        end
        output *= board[i+1] * " "
    end
    println(output)
end


@inline function find_goal(board)
    board = sort(collect(board))
    push!(board, popfirst!(board))
    return join(board)
end

@inline function goal_test(test)
    if test == find_goal(test)
        return true
    end
    return false
end

@inline function twoToOne(x, y, boardSize)
    return x + (y * boardSize)
end

@inline function oneToTwo(index, boardSize)
    return mod(index, boardSize), index ÷ boardSize
end

@inline function swap(toSwap, pos, posSwap)
    toSwap[pos+1], toSwap[posSwap+1] = toSwap[posSwap+1], toSwap[pos+1]
    return join(toSwap)
end

function taxicab(board)
    boardSize = sqrt(length(board))
    goal = find_goal(board)
    count = 0
    for value in board
        if value != '.'
            x, y = oneToTwo(findfirst(isequal(value), board) - 1, boardSize)
            xg, yg = oneToTwo(findfirst(isequal(value), goal) - 1, boardSize)
            count += abs(yg - y) + abs(xg - x)
        end
    end
    return count
end

@inline function taxicab2(char, indexOx, indexOy, indexNx, indexNy, old)
    posGx, posGy = loc[char]
    if abs(posGx - indexOx) + abs(posGy - indexOy) >
       abs(posGx - indexNx) + abs(posGy - indexNy)
        return old - 1
    else
        return old + 1
    end
end

function inversionCount(board)
    board = replace(board, "." => "")
    copyBoard = board
    count = 0
    for x in board[2:end]
        while copyBoard[findfirst(isequal(x), copyBoard)-1] > x &&
            findfirst(isequal(x), copyBoard) - 2 > 0
            switch = collect(copyBoard)
            xPos = findfirst(isequal(x), switch)
            temp = switch[xPos-1]
            switch[xPos] = temp
            switch[xPos-1] = x
            copyBoard = join(switch)
            count += 1
        end
    end
    return count
end

function parityCheck(board)
    boardSize = sqrt(length(board))
    even = mod(boardSize, 2)
    count = inversionCount(board)
    if even == 0
        x, y = oneToTwo(findfirst(isequal('.'), board) - 1, boardSize)
        if mod(count, 2) == 0
            if mod((boardSize - y), 2) == 0
                return false
            end
        else
            if mod(boardSize - y, 2) == 1
                return false
            end
        end
    else
        if mod(count, 2) == 1
            return false
        end
    end
    return true
end

@inline function rcCount(col, rowNum, char, state)
    total = 0
    total2 = 0
    conflicts = []
    conflicts2 = []
    goalc, goalr = loc[char]
    for i = 0:3
        spot = i + (rowNum * 4)
        spot2 = col + (i * 4)
        if state[spot+1] != '.' && i != col
            goalTc, goalTr = loc[state[spot+1]]
            if i < col
                if goalTc > goalc && goalTr == goalr && goalr == rowNum
                    push!(conflicts, mod(spot, 4))
                    total += 1
                end
            else
                if goalTc < goalc && goalTr == goalr && goalr == rowNum
                    push!(conflicts, mod(spot, 4))
                    total += 1
                end
            end
        end
        if state[spot2+1] != '.' && i != rowNum
            goalTc, goalTr = loc[state[spot2+1]]
            if i < rowNum
                if goalTr > goalr && goalTc == goalc && goalc == col
                    push!(conflicts2, spot2 ÷ 4)
                    total2 += 1
                end
            else
                if goalTr < goalr && goalTc == goalc && goalc == col
                    push!(conflicts2, spot2 ÷ 4)
                    total2 += 1
                end
            end
        end
    end
    rValue = (total, conflicts, total2, conflicts2)
    return rValue
end

function linearC(state)
    total = 0
    colSaves = []
    conflictPos = []
    for i = 0:3
        tileConflict = []
        for j = 0:3
            spot = j + (i * 4)
            if state[spot+1] != '.'
                val, conflicts, val2, conflicts2 =
                    rcCount(j, i, state[spot+1], state)
                push!(tileConflict, [val, conflicts])
                push!(colSaves, [val2, conflicts2])
            else
                push!(tileConflict, [0, []])
                push!(colSaves, [0, []])
            end
        end
        value = maximum(tileConflict)
        while value[1] != 0
            push!(conflictPos, (i, true))
            pos = findfirst(isequal(value), tileConflict)
            for y in tileConflict[pos][2]
                tileConflict[y+1][1] -= 1
                deleteat!(
                    tileConflict[y+1][2],
                    findfirst(isequal(pos - 1), tileConflict[y+1][2]),
                )
            end
            value[1], value[2] = 0, []
            total += 1
            value = maximum(tileConflict)
        end
    end
    for i = 0:3
        temp = colSaves[i+1:4:end]
        value = maximum(temp)
        while value[1] != 0
            push!(conflictPos, (i, false))
            value = maximum(temp)
            pos = findfirst(isequal(value), temp)
            for y in temp[pos][2]
                temp[y+1][1] -= 1
                deleteat!(
                    temp[y+1][2],
                    findfirst(isequal(pos - 1), temp[y+1][2]),
                )
            end
            value[1], value[2] = 0, []
            total += 1
        end
    end
    final = total * 2
    return final, conflictPos
end

@inline function linearC2(
    state,
    conflicts,
    newSpotx,
    newSpoty,
    oldSpotx,
    oldSpoty,
    old,
    direction,
)
    returnValue = old
    total = 0
    rowC = colC = false
    conflictPos = union(conflicts) #Did not know how to do this with dictionary, so used union instead to remove duplicates
    if direction
        for i in conflictPos
            pos, row = i
            if !row && oldSpotx == pos
                colC = true
                deleteat!(conflictPos, findfirst(isequal(i), conflictPos))
                returnValue -= 2
            end
            if !row && newSpotx == pos
                deleteat!(conflictPos, findfirst(isequal(i), conflictPos))
                returnValue -= 2
            end
        end
        spot = newSpotx + (newSpoty * 4)
        g1, g2, value, conflicts =
            rcCount(newSpotx, newSpoty, state[spot+1], state)
        if value != 0 || colC
            colSaves = []
            colOld = []
            for i = 0:3
                g1, g2, val, conflicts =
                    rcCount(newSpotx, i, state[newSpotx+(i*4)+1], state)
                push!(colSaves, [val, conflicts])
                if colC
                    spot = oldSpotx + (i * 4)
                    if state[spot+1] != '.'
                        g1, g2, val, conflicts =
                            rcCount(oldSpotx, i, state[oldSpotx+(i*4)+1], state)
                        push!(colOld, [val, conflicts])
                    else
                        push!(colOld, [0, []])
                    end
                end
            end
            value = maximum(colSaves)
            while value[1] != 0
                push!(conflictPos, (newSpotx, false))
                value = maximum(colSaves)
                pos = findfirst(isequal(value), colSaves)
                for y in colSaves[pos][2]
                    colSaves[y+1][1] -= 1
                    deleteat!(
                        colSaves[y+1][2],
                        findfirst(isequal(pos - 1), colSaves[y+1][2]),
                    )
                end
                value[1], value[2] = 0, []
                total += 1
            end
            if colC
                value = maximum(colOld)
                while value[1] != 0
                    push!(conflictPos, (newSpotx, false))
                    value = maximum(colSaves)
                    pos = findfirst(isequal(value), colSaves)
                    for y in colSaves[pos][2]
                        colSaves[y+1][1] -= 1
                        deleteat!(
                            colSaves[y+1][2],
                            findfirst(isequal(pos - 1), colSaves[y+1][2]),
                        )
                    end
                    value[1], value[2] = 0, []
                    total += 1
                end
            end
        end
    else
        for i in conflictPos
            pos, row = i
            if row && oldSpoty == pos
                rowC = true
                deleteat!(conflictPos, findfirst(isequal(i), conflictPos))
                returnValue -= 2
            end
            if row && newSpoty == pos
                deleteat!(conflictPos, findfirst(isequal(i), conflictPos))
                returnValue -= 2
            end
        end
        spot = newSpotx + (newSpoty * 4)
        value, conflicts, g1, g2 =
            rcCount(newSpotx, newSpoty, state[spot+1], state)
        if value != 0 || rowC
            rowSaves = []
            rowOld = []
            for i = 0:3
                value, conflicts, g1, g2 =
                    rcCount(i, newSpoty, state[i+(newSpoty*4)+1], state)
                push!(rowSaves, [value, conflicts])
                if rowC
                    spot = i + (oldSpoty * 4)
                    if state[spot+1] != '.'
                        value, conflicts, g1, g2 =
                            rcCount(i, oldSpoty, state[i+(oldSpoty*4)+1], state)
                        push!(rowOld, [value, conflicts])
                    else
                        push!(rowOld, [0, []])
                    end
                end
            end
            value = maximum(rowSaves)
            while value[1] != 0
                push!(conflictPos, (newSpoty, true))
                value = maximum(rowSaves)
                pos = findfirst(isequal(value), rowSaves)
                for y in rowSaves[pos][2]
                    rowSaves[y+1][1] -= 1
                    deleteat!(
                        rowSaves[y+1][2],
                        findfirst(isequal(pos - 1), rowSaves[y+1][2]),
                    )
                end
                value[1], value[2] = 0, []
                total += 1
            end
            if rowC
                value = maximum(rowOld)
                while value[1] != 0
                    push!(conflictPos, (newSpoty, false))
                    value = maximum(rowOld)
                    pos = findfirst(isequal(value), rowOld)
                    for y in rowOld[pos][2]
                        rowOld[y+1][1] -= 1
                        deleteat!(
                            rowOld[y+1][2],
                            findfirst(isequal(pos - 1), rowOld[y+1][2]),
                        )
                    end
                    value[1], value[2] = 0, []
                    total += 1
                end
            end
        end
    end
    returnValue += total * 2
    return returnValue, conflictPos
end

@inline function get_children(parent)
    children = []
    boardSize = sqrt(length(parent))
    pos = findfirst(isequal('.'), parent) - 1
    posx, posy = mod(pos, 4), pos ÷ 4
    if posx + 1 <= boardSize - 1
        push!(
            children,
            (
                swap(collect(parent), pos, posx + 1 + (posy * 4)),
                posx + 1,
                posy,
                posx,
                posy,
                true,
            ),
        )
    end
    if posx - 1 >= 0
        push!(
            children,
            (
                swap(collect(parent), pos, posx - 1 + (posy * 4)),
                posx - 1,
                posy,
                posx,
                posy,
                true,
            ),
        )
    end
    if posy + 1 <= boardSize - 1
        push!(
            children,
            (
                swap(collect(parent), pos, posx + (posy + 1) * 4),
                posx,
                posy + 1,
                posx,
                posy,
                false,
            ),
        )
    end
    if posy - 1 >= 0
        push!(
            children,
            (
                swap(collect(parent), pos, posx + (posy - 1) * 4),
                posx,
                posy - 1,
                posx,
                posy,
                false,
            ),
        )
    end
    return children
end


function astar(start)
    closed = Set()
    conflicts, spots = linearC(start)
    data =
        (taxicab(start) + conflicts, start, 0, taxicab(start), conflicts, spots)
    fringe = BinaryMinHeap{Tuple}()
    push!(fringe, data)
    while length(fringe) != 0
        heuristic, state, depth, trueHeuristic, saves, wheres = pop!(fringe)
        if goal_test(state)
            return depth
        end
        if !(state in closed)
            push!(closed, state)
            listChildren = get_children(state)
            #shuffle!(listChildren)
            for child in listChildren
                new_State, posOx, posOy, posNx, posNy, direction = child
                if !(new_State in closed)
                    t2 = taxicab2(
                        state[posOx+(posOy*4)+1],
                        posOx,
                        posOy,
                        posNx,
                        posNy,
                        trueHeuristic,
                    )
                    val, place = linearC2(
                        new_State,
                        wheres,
                        posNx,
                        posNy,
                        posOx,
                        posOy,
                        saves,
                        direction,
                    )
                    new_data = (
                        depth + 1 + t2 + val,
                        new_State,
                        depth + 1,
                        t2,
                        val,
                        place,
                    )
                    push!(fringe, new_data)
                end
            end
        end
    end
    return nothing
end

function runProgram()
    #f = open("15_puzzles.txt")
    f = open(ARGS[1])
    lines = readlines(f)
    close(f)
    totalStart = time()
    lineCounter = 0
    for line in lines
        strip(line)
        #=
        I could not use parityCheck beacuse I realized that my python code for it was wrong,
        and would sometimes used -1 as an index, but beacuse python allows for negative steps/indexing it still worked fine.
        Julia does not allow for 0 or negative indicies so using parityCheck would require creating a completely new method
        =#
        start = time()
        moves = astar(line)
        toPrint = @sprintf(
            "Lines %s: %s, A* - %s moves in %s seconds",
            lineCounter,
            line,
            moves,
            time() - start
        )
        println(toPrint)
        lineCounter += 1
    end
    println(time() - totalStart)
end

runProgram()
