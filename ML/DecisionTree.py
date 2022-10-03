import math
from collections import Counter
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

    def alphabeticalSort(self):
        zipped = zip(self.features, self.children)
        sortedPairs = sorted(zipped)
        tuples = zip(*sortedPairs)
        self.features, self.children = [list(tup) for tup in tuples]


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
        else:
            removeIndices = {i for i, x in enumerate(data[maxInfoIndex]) if x != feature}
            copyData = [x.copy() for x in data]
            for index, dataSet in enumerate(copyData):
                copyData[index] = [i for j, i in enumerate(dataSet) if j not in removeIndices]
            sNode.children.append(genTree(copyData, features))
    return sNode


def inputData(filename):
    dataStored = []
    with open(filename) as f:
        for lineNum, line in enumerate(f):
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
            #print("\t" * (tabSpace - 1) + "  ", "* %s" % featureName)
            #print("\t" * (tabSpace - 1) + "    ", "* %s?" % tree.featureSplitName)
            f.write("\t" * (tabSpace - 1) + "  " + "* %s" % featureName + "\n")
            f.write("\t" * (tabSpace - 1) + "    " + "* %s?" % tree.featureSplitName + "\n")
        else:
            #print("\t" * tabSpace, "* %s?" % tree.featureSplitName)
            f.write("\t" * tabSpace + "* %s?" % tree.featureSplitName + "\n")
        tabSpace += 1
        for index, child in enumerate(tree.children):
            printTree(child, tabSpace, tree.features[index])
    else:
        #print("\t" * (tabSpace - 1) + "  ", "* %s --> %s" % (featureName, tree.output))
        f.write("\t" * (tabSpace - 1) + "  " + "* %s --> %s" % (featureName, tree.output) + "\n")


a, b, c = inputData("mushroom.csv")
decisionTree = genTree(a, b)
f = open('treeout.txt', 'w')
printTree(decisionTree, 0, None, True)
