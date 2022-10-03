import numpy as np
import math
import random
import sys
import ast


def step(num):
    if num > 0:
        return 1
    return 0


def sigmoid(num):
    return 1 / (1 + (math.e ** (-num)))


def p_net(A, x, wList, bList):
    A = np.vectorize(A)
    layers = [x]
    for index in range(1, len(wList)):
        layerOutput = A((layers[index - 1] @ wList[index]) + bList[index])
        layers.append(layerOutput)
    return layers[len(layers) - 1]


def xor(inputs):  # XOR HAPPENS HERE
    wList = [None, np.array([[1, -1], [-1, 1]]), np.array([[1], [1]])]
    bList = [None, np.array([-.5, -.5]), np.array([-.5])]
    return p_net(step, inputs, wList, bList)


def diamond(inputs):
    wList = [None, np.array([[1, -1, 1, -1], [1, 1, -1, -1]]), np.array([[1], [1], [1], [1]])]
    bList = [None, np.array([-1, -1, -1, -1]), np.array([-.5])]
    output = p_net(step, inputs, wList, bList)
    if output == 0:
        print('Inside')
    else:
        print('Outside')


def circle(inputs):
    wList = [None, np.array([[1, -1, 1, -1], [1, 1, -1, -1]]), np.array([[1], [1], [1], [1]])]
    bList = [None, np.array([2.3, 2.3, 2.3, 2.3]), np.array([-3.5])]
    return round(p_net(sigmoid, inputs, wList, bList)[0])


def testDiamond(inputs):
    x = [random.uniform(-1, 1) for num in range(500)]
    y = [random.uniform(-1, 1) for num in range(500)]
    correct = total = 0
    for i in range(500):
        total += 1
        output = diamond(np.array([x[i], y[i]]))
        if abs(x[i]) + abs(y[i]) < 1 and output == 0:
            correct += 1
        elif abs(x[i]) + abs(y[i]) >= 1 and output == 1:
            correct += 1
    print(correct / total)


def testCircle():
    x = [random.uniform(-1, 1) for num in range(500)]
    y = [random.uniform(-1, 1) for num in range(500)]
    correct = total = 0
    misclassified = []
    for i in range(500):
        total += 1
        output = circle(np.array([x[i], y[i]]))
        if math.sqrt(pow(x[i], 2) + pow(y[i], 2)) < 1 and output == 1:
            correct += 1
        elif math.sqrt(pow(x[i], 2) + pow(y[i], 2)) >= 1 and output == 0:
            correct += 1
        else:
            misclassified.append((x[i], y[i]))
    print('Accuracy %s' % (correct / total))
    print('Misclassified', misclassified)


if len(sys.argv) == 2:
    print(xor(np.array(list(ast.literal_eval(sys.argv[1]))))[0])
elif len(sys.argv) == 3:
    diamond(np.array([float(sys.argv[1]), float(sys.argv[2])]))
else:
    testCircle()
