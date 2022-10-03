import numpy as np
import math
import random
import sys
import pickle


def sigmoid(x):
    if x < 0:
        a = np.exp(x)
        return a / (1 + a)
    else:
        return 1 / (1 + np.exp(-x))


def sigmoidPrime(x):
    return sigmoid(x) * (1 - sigmoid(x))


def p_net(A, x, wList, bList):
    A = np.vectorize(A)
    layers = [x]
    dots = [None]
    for index in range(1, len(wList)):
        dots.append((layers[index - 1] @ wList[index]) + bList[index])
        layerOutput = A(dots[index])
        layers.append(layerOutput)
    return layers, dots


def wnbgen(arch):
    wList = [None, 2 * np.random.rand(arch[0], arch[1]) - 1, 2 * np.random.rand(arch[1], arch[2]) - 1,
             2 * np.random.rand(arch[2], arch[3]) - 1]
    bList = [None, 2 * np.random.rand(1, arch[1]) - 1, 2 * np.random.rand(1, arch[2]) - 1,
             2 * np.random.rand(1, arch[3]) - 1]
    return wList, bList


def mnist():
    test = []
    known = []
    with open("mnist_test.csv") as f:
        for line in f:
            data = list(map(int, line.strip().split(',')))
            known.append(np.array([[data[0]]]))
            test.append(np.array([data[1:]]))
    with open('MNISTWB.pickle', 'rb') as f:
        data = pickle.load(f)
    wList = data[0]
    bList = data[1]
    index = total = correct = 0
    for ins, outs in zip(test, known):
        layers, dots = p_net(sigmoid, ins, wList, bList)
        if known[index][0][0] == np.argmax(layers[len(layers) - 1]):
            correct += 1
        total += 1
        index += 1
    print(correct / total)


mnist()
