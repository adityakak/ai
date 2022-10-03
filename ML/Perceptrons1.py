import sys
import ast


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


print(check(int(sys.argv[1]), ast.literal_eval(sys.argv[2]), float(sys.argv[3])))
