import sys
import ast
import math
import time

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


def perceptronInit(bits):
    total = correct = 0
    for i in range(pow(2, pow(2, bits))):
        truth = truthTable(bits, i)
        w, b, acc = trainPerceptron(truth, i)
        if acc == 1:
            correct += 1
        total += 1
    print("%s possible functions; %s can be correctly modeled" % (total, correct))


def xor(inputs):  # XOR HAPPENS HERE
    """
    perceptronW3 = (1, -1)
    perceptronB3 = -.5

    perceptronW4 = (-1, 1)
    perceptronB4 = -.5

    perceptronW5 = (1, 1)
    perceptronB5 = -.5
    """
    perceptronW3 = (-1, 1)
    perceptronB3 = .5

    perceptronW4 = (1, -1)
    perceptronB4 = .5

    perceptronW5 = (-1, -1)
    perceptronB5 = 1

    perceptron3Output = perceptron(step, perceptronW3, perceptronB3, inputs)
    perceptron4Output = perceptron(step, perceptronW4, perceptronB4, inputs)

    perceptron5Output = perceptron(step, perceptronW5, perceptronB5, (perceptron3Output, perceptron4Output))
    return perceptron5Output


print(xor((1, 0)))
# print(xor(ast.literal_eval(sys.argv[1])))
