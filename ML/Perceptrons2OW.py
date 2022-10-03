import sys
import ast
import math
import time
from matplotlib import pyplot as plt

epochs = 100


def genBinStrings(string, length, pos):
    generated = []
    if length == pos:
        return string
    string[pos] = 0
    generated.extend(genBinStrings(string, length, pos + 1))
    string[pos] = 1
    generated.extend(genBinStrings(string, length, pos + 1))
    return generated


def truthTable(bits, n):
    generatedCombinations = genBinStrings([None] * bits, bits, 0)
    tuples = [tuple(generatedCombinations[i:i + bits]) for i in range(0, len(generatedCombinations), bits)]
    tuples.sort(reverse=True, key=lambda tup: int(''.join(map(str, tup))))
    binaryNumber = bin(n)[2:].zfill(pow(2, bits))
    truths = {}
    for index, inputs in enumerate(tuples):
        truths[inputs] = binaryNumber[index]
    return truths


def prettyPrintTable(table):
    output = ''
    inputCount = len(list(table.keys())[0])
    for j in range(inputCount + 1):
        if j == inputCount:
            output += 'Out' + '\n'
        else:
            output += "In " + str(j + 1) + '\t'
    for index, i in enumerate(table.keys()):
        for inputs in i:
            output += str(inputs) + '\t' + '\t'
        output += str(table[i]) + '\n'
    print(output)


def step(num):
    if num > 0:
        return 1
    return 0


def dot(a, b):
    return sum(i * j for i, j in zip(a, b))


def perceptron(A, w, b, x):
    return A(dot(w, x) + b)


def check(n, w, b):
    correct = total = 0
    table = truthTable(len(w), n)
    for inputs in table.keys():
        perceptronOutput = perceptron(step, w, b, inputs)
        if perceptronOutput == int(table[inputs]):
            correct += 1
        total += 1
    return correct / total


def createGroups(lists, bits):
    return [lists[i: i + bits] for i in range(0, len(lists), bits)]


def scalarMultiply(scalar, vector):
    returnValue = []
    for value in vector:
        returnValue.append(scalar * value)
    return tuple(returnValue)


def vectorAdd(v1, v2):
    returnValue = []
    for i in range(len(v1)):
        returnValue.append(v1[i] + v2[i])
    return tuple(returnValue)


def trainPerceptron(table, n):
    w = tuple([0] * len(list(table.keys())[0]))
    b = 0
    prevW = prevB = None
    for i in range(epochs):
        for val in list(table.keys()):
            curr = perceptron(step, w, b, val)
            outputDiff = int(table[val]) - curr
            w = vectorAdd(w, scalarMultiply(outputDiff, val))
            b += outputDiff
        if prevW == w and prevB == b:
            return w, b, check(n, w, b)
        prevW = w
        prevB = b
    return w, b, check(n, w, b)


def perceptronInit():
    bits = 2
    count = 0
    for i in range(pow(2, pow(2, bits))):
        truth = truthTable(bits, i)
        w, b, acc = trainPerceptron(truth, i)
        xVal = []
        yVal = []
        cVal = []
        sVal = []
        initialX = -2
        initialY = -2
        while initialY < 2:
            while initialX < 2:
                xVal.append(initialX)
                yVal.append(initialY)
                if (initialX, initialY) in truth.keys():
                    cVal.append('g' if int(truth[(initialX, initialY)]) == 0 else 'r')
                    sVal.append(20 * 4 * 2)
                else:
                    cVal.append('g' if perceptron(step, w, b, (initialX, initialY)) == 0 else 'r')
                    sVal.append(20 * 4 * .1)
                initialX += .1
                initialX = round(initialX, 1)
            initialX = -2
            initialY += .1
            initialY = round(initialY, 1)
        plt.title("Function #%s" % count)
        plt.scatter(xVal, yVal, c=cVal, s=sVal)
        plt.show()
        count += 1


perceptronInit()
