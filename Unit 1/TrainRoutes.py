import sys
from time import perf_counter
from math import pi, acos, sin, cos
import heapq
import tkinter as tk
import copy
import random

start = perf_counter()
keyJunctions = {}
nodes = {}
normalNodes = {}
connections = {}
lines = {}


def circleDistance(node1, node2):
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees
    y1, x1 = node1
    y2, x2 = node2

    R = 3958.76  # miles = 6371 km
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0

    # approximate great circle distance with law of cosines
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


def trace_path(parents, goal_state, start_state):
    path = [goal_state]
    node = goal_state
    while node != start_state:
        path.append(parents[node])
        node = path[-1]
    path.reverse()
    prev = None
    for n in path:
        if prev is None:
            prev = n
        else:
            canvas.itemconfig(lines[(prev, n)], fill="red")
            canvas.itemconfig(lines[(n, prev)], fill="red")
            prev = n


def dijkstra(s, e):
    sTime = perf_counter()
    closed = {""}
    dictionary = {s: None}
    data = (0, s, random.uniform(0, 1), dictionary)
    fringe = []
    heapq.heappush(fringe, data)
    count = 0
    while len(fringe) != 0:
        depth, spot, randoms, parents = heapq.heappop(fringe)
        if spot == e:
            eTime = perf_counter()
            trace_path(parents, spot, s)
            return depth, (eTime - sTime)
        if spot not in closed:
            closed.add(spot)
            for child in connections[spot]:
                cNode, distance = child
                canvas.itemconfig(lines[(spot, cNode)], fill="blue")
                if cNode not in closed:
                    parents[cNode] = spot
                    new_data = (depth + distance, cNode, random.uniform(0, 1), copy.copy(parents))
                    heapq.heappush(fringe, new_data)
                    if count % 700 == 0:
                        root.update()
                    count += 1
    return None, None


def astar(s, e):
    sTime = perf_counter()
    closed = {""}
    dictionary = {s: None}
    data = (circleDistance(nodes[s], nodes[e]), 0, s, random.uniform(0, 1), dictionary)
    fringe = []
    count = 0
    heapq.heappush(fringe, data)
    while len(fringe) != 0:
        heuristic, depth, spot, randoms, parents = heapq.heappop(fringe)
        if spot == e:
            eTime = perf_counter()
            trace_path(parents, spot, s)
            return depth, (eTime - sTime)
        if spot not in closed:
            closed.add(spot)
            for child in connections[spot]:
                cNode, distance = child
                canvas.itemconfig(lines[(spot, cNode)], fill="blue")
                if cNode not in closed:
                    parents[cNode] = spot
                    val = depth + distance
                    new_data = (circleDistance(nodes[cNode], nodes[e]) + val, val, cNode, random.uniform(0, 1), copy.copy(parents))
                    heapq.heappush(fringe, new_data)
                    if count % 700 == 0:
                        root.update()
                    count += 1
    return None, None


def createGrid(s):
    a = 800 / (60.84682 - 14.68673)
    b = 800 - (a * 60.84682)
    a2 = 800 / (-60.02403 + 130.35722)
    b2 = 800 - (a2 * -60.02403)
    for i in nodes.keys():
        x, y = nodes[i]
        normalNodes[i] = ((a * x) + b, (a2 * y) + b2)
    for i in connections.keys():
        for j in connections[i]:
            num, garbage = j
            x, y = normalNodes[i]
            x2, y2 = normalNodes[num]
            lines[(i, num)] = s.create_line(y, 800 - x, y2, 800 - x2, tag='grid_line')


with open("rrNodeCity.txt") as f:
    for line in f:
        split = line.strip().split()
        word = ""
        for x in split[1::]:
            word += x
            word += ' '
        keyJunctions[word.strip()] = split[0]

with open("rrNodes.txt") as f:
    for line in f:
        split = line.strip().split()
        nodes[split[0]] = (float(split[1]), float(split[2]))

with open("rrEdges.txt") as f:
    for line in f:
        node1, node2 = line.strip().split()
        dis = circleDistance(nodes[node1], nodes[node2])
        if node1 in connections:
            connections[node1].append((node2, dis))
        else:
            connections[node1] = [(node2, dis)]
        if node2 in connections:
            connections[node2].append((node1, dis))
        else:
            connections[node2] = [(node1, dis)]

end = perf_counter()
print("Time to create data structure: %s seconds" % (end - start))

root = tk.Tk()
canvas = tk.Canvas(root, height=800, width=800, bg='white')
createGrid(canvas)
canvas.pack(expand=True)
root.update()

dis, time = dijkstra(keyJunctions[sys.argv[1]], keyJunctions[sys.argv[2]])
print(sys.argv[1], "to", sys.argv[2], "with Dijkstra: %s in %s seconds" % (dis, time))
root.mainloop()

root = tk.Tk()
canvas = tk.Canvas(root, height=800, width=800, bg='white')
createGrid(canvas)
canvas.pack(expand=True)
root.update()

dis2, time2 = astar(keyJunctions[sys.argv[1]], keyJunctions[sys.argv[2]])
print(sys.argv[1], "to", sys.argv[2], "with A*: %s in %s seconds" % (dis2, time2))
root.mainloop()

'''
root = tk.Tk()
canvas = tk.Canvas(root, height=800, width=800, bg='white')
createGrid(canvas)
canvas.pack(expand=True)
root.update()


start = 'Ciudad Juarez'
end = 'Montreal'

dis, time = dijkstra(keyJunctions[start], keyJunctions[end])
root.mainloop()

root = tk.Tk()
canvas = tk.Canvas(root, height=800, width=800, bg='white')
createGrid(canvas)
canvas.pack(expand=True)
root.update()
dis2, time2 = astar(keyJunctions[start], keyJunctions[end])
root.mainloop()

print(start, "to", end, "with Dijkstra: %s in %s seconds" % (dis, time))
print(start, "to", end, "with A*: %s in %s seconds" % (dis2, time2))
'''
