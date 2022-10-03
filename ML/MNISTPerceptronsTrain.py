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
    training = []
    known = []
    with open("mnist_train.csv") as f:
        for line in f:
            data = list(map(int, line.strip().split(',')))
            answer = np.array([[data[0]]])
            known.append(np.array([[0 if x != answer[0][0] else 1 for x in range(10)]]))
            training.append(np.array([data[1:]]))
    wList, bList = wnbgen([784, 300, 100, 10])
    localLearningRate = .1
    derivative = np.vectorize(sigmoidPrime)
    for i in range(1000):
        for ins, outs in zip(training, known):
            layers, dots = p_net(sigmoid, ins, wList, bList)
            deltaL = [None] * (len(wList) - 1)
            deltaL[len(deltaL) - 1] = derivative(dots[len(dots) - 1]) * (outs - layers[len(layers) - 1])
            for l in range(len(layers) - 2, 0, -1):
                deltaL[l - 1] = (derivative(dots[l]) * (deltaL[l] @ np.transpose(wList[l + 1])))
            for layerNumber, l in enumerate(deltaL):
                bList[layerNumber + 1] = bList[layerNumber + 1] + (localLearningRate * l)
                wList[layerNumber + 1] = wList[layerNumber + 1] + (localLearningRate * (np.transpose(layers[layerNumber]) @ l))
        dumping = [wList, bList]
        with open('MNISTWB.pickle', 'wb') as f:
            pickle.dump(dumping, f)
            print("Epoch %s Dumped" % (i + 1))


mnist()
