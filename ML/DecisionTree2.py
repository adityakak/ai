from matplotlib import pyplot as plt
import random
import math
from collections import Counter
import time
import sys


class Node:
    def __init__(self, featureValues, featureName, isLeaf=False, output=None):
        if isLeaf:
            self.output = output
            self.isLeaf = True
        else:
            self.numFeatures = len(featureValues)
            self.features = featureValues
            self.featureSplitName = featureName
            self.children = []
            self.isLeaf = False

    def cleanFeatures(self):
        self.features = list(self.features)

    def alphabeticalSort(self):
        zipped = zip(self.features, self.children)
        sortedPairs = sorted(zipped)
        tuples = zip(*sortedPairs)
        self.features, self.children = [list(tup) for tup in tuples]

    """
    def __copy__(self):
        if self.isLeaf:
            return Node(None, None, True, output=self.output)
        else:
            temp = Node(self.features.copy(), self.featureSplitName)
            temp.setChildren(self.children)
            return temp
    """


def entropy(outcomes, feature):
    total = 0
    uniqueOutcomes = Counter(outcomes).keys()
    if feature is None:
        for unique in uniqueOutcomes:
            uniqueCount = outcomes.count(unique)
            total += uniqueCount / len(outcomes) * math.log(uniqueCount / len(outcomes), 2)
        return total * -1
    else:
        uniqueFeatures = Counter(feature).keys()
        for unique in uniqueFeatures:
            indices = [i for i, x in enumerate(feature) if x == unique]
            entropyCalc = []
            for index in indices:
                entropyCalc.append(outcomes[index])
            total += len(indices) / len(feature) * entropy(entropyCalc, None)
        return total


def infoGain(outcomes, feature):
    return entropy(outcomes, None) - entropy(outcomes, feature)


def genTree(data, features):
    maxInfoGain = []
    for index, feature in enumerate(features):
        maxInfoGain.append(infoGain(data[len(data) - 1], data[index]))
    maxInfo = max(maxInfoGain)
    maxInfoIndex = maxInfoGain.index(maxInfo)
    sNode = Node(Counter(data[maxInfoIndex]).keys(), features[maxInfoIndex])
    for childIndex, feature in enumerate(sNode.features):
        featureEntropy = entropy(
            [x for index, x in enumerate(data[len(data) - 1]) if data[maxInfoIndex][index] == feature], None)
        if featureEntropy == 0:
            sNode.children.append(Node(None, None, True, data[len(data) - 1][data[maxInfoIndex].index(feature)]))
        elif all(v == 0 for v in maxInfoGain):
            sNode.children.append(Node(None, None, True, random.choice(data[len(data) - 1])))
        else:
            removeIndices = {i for i, x in enumerate(data[maxInfoIndex]) if x != feature}
            copyData = [x.copy() for x in data]
            for index, dataSet in enumerate(copyData):
                copyData[index] = [i for j, i in enumerate(dataSet) if j not in removeIndices]
            sNode.children.append(genTree(copyData, features))
    return sNode


def inputData(filename):
    dataStored = []
    with open(filename) as file:
        for lineNum, line in enumerate(file):
            if lineNum == 0:
                featureNames = line.strip().split(',')
                for name in featureNames:
                    dataStored.append([])
            else:
                dataValues = line.strip().split(',')
                for index, value in enumerate(dataValues):
                    dataStored[index].append(value)
    answerHeader = featureNames[-1]
    del featureNames[-1]
    return dataStored, featureNames, answerHeader


def printTree(tree, tabSpace=0, featureName=None, isHead=False):
    if tree.isLeaf is False:
        tree.alphabeticalSort()
        if not isHead:
            print("\t" * (tabSpace - 1) + "  ", "* %s" % featureName)
            print("\t" * (tabSpace - 1) + "    ", "* %s?" % tree.featureSplitName)
            # f.write("\t" * (tabSpace - 1) + "  " + "* %s" % featureName + "\n")
            # f.write("\t" * (tabSpace - 1) + "    " + "* %s?" % tree.featureSplitName + "\n")
        else:
            print("\t" * tabSpace, "* %s?" % tree.featureSplitName)
            # f.write("\t" * tabSpace + "* %s?" % tree.featureSplitName + "\n")
        tabSpace += 1
        for index, child in enumerate(tree.children):
            printTree(child, tabSpace, tree.features[index])
    else:
        print("\t" * (tabSpace - 1) + "  ", "* %s --> %s" % (featureName, tree.output))
        # f.write("\t" * (tabSpace - 1) + "  " + "* %s --> %s" % (featureName, tree.output) + "\n")


def testTree(test, tree, featureNames):
    correct = 0
    #printTree(tree, 0, None, True)
    for testData in test:
        nodeCopy = tree
        while nodeCopy.isLeaf is not True:
            nodeCopy.cleanFeatures()
            splitFeatureIndex = featureNames.index(nodeCopy.featureSplitName)
            try:
                featureValue = testData[splitFeatureIndex]
                childIndex = nodeCopy.features.index(featureValue)
                nodeCopy = nodeCopy.children[childIndex]
            except ValueError:
                nodeCopy = random.choice(nodeCopy.children)
        if testData[len(testData) - 1] == nodeCopy.output:
            correct += 1
    return correct / len(test)


def readData(filename):
    nonMissing = []
    missing = []
    with open(filename) as f:
        for lineNum, line in enumerate(f):
            if lineNum != 0:
                data = line.strip().split(",")
                if "?" not in data:
                    nonMissing.append(data)
                else:
                    missing.append(data)
            else:
                featureNames = line.strip().split(',')
    return missing, nonMissing, featureNames


def dataManipulation(missing, nonMissing, featureNames):
    repeat = True
    toMakeSize = len(featureNames)
    answerHeader = featureNames[-1]
    # del featureNames[0]
    del featureNames[-1]
    """
    majorityVote = [[0, 0] for x in range(len(storeData) - 1)]
    for featureIndex, data in enumerate(storeData):
        if featureIndex != len(storeData) - 1:
            for voteIndex, vote in enumerate(data):
                if storeData[len(storeData) - 1][voteIndex] == 'democrat':
                    tmpIndex = 0
                else:
                    tmpIndex = 1
                if vote == 'y':
                    majorityVote[featureIndex][tmpIndex] += 1
                else:
                    majorityVote[featureIndex][tmpIndex] -= 1
    for missingData in missing:
        del missingData[0]
        missingLocations = [x for x in range(len(missingData)) if missingData[x] == "?"]
        classification = missingData[len(missingData) - 1]
        if classification == 'democrat':
            voteIndex = 0
        else:
            voteIndex = 1
        for missingIndex in missingLocations:
            missingData[missingIndex] = 'n' if majorityVote[missingIndex][voteIndex] < 0 else 'y'
    for data in missing:
        for index, value in enumerate(data):
            storeData[index].append(value)
    """
    totalData = nonMissing + missing
    random.shuffle(totalData)
    storeData = [[] for x in range(toMakeSize)]
    for data in totalData:
        # del data[0]
        for index, value in enumerate(data):
            storeData[index].append(value)
    test = totalData[len(totalData) - int(sys.argv[2]): len(totalData)]
    possibleTrain = totalData[0: len(totalData) - int(sys.argv[2])]
    accuracy = []
    for size in range(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])):
        train = []
        while repeat:
            train = random.sample(range(0, len(possibleTrain)), size)
            checkSame = set()
            for dataPiece in train:
                checkSame.add(storeData[toMakeSize - 1][dataPiece])
            if len(checkSame) >= 2:
                repeat = False
        outputTree = genTree([[storeData[x][y] for y in train] for x in range(len(storeData))], featureNames)
        # printTree(outputTree, 0, None, True)
        accuracy.append(testTree(test, outputTree, featureNames) * 100)
        repeat = True
        #print(size)
    plt.scatter([x for x in range(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))], accuracy)
    plt.xlabel('Training Set Size')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy vs Training Set Size for Connect-Four')
    #print(time.perf_counter() - s)
    plt.show()


s = time.perf_counter()
a, b, c = readData(sys.argv[1])
dataManipulation(a, b, c)
