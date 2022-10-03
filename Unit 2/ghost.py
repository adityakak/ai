import sys
import time as ti
import string


def possible_next_strings(line):
    alphabet = list(string.ascii_uppercase)
    children = []
    for letter in alphabet:
        temp = line + letter
        if temp in substrings:
            children.append((temp, letter))
    return children


def is_over(line, player):
    if line in dictionary:
        if player == 1:
            return True, 1
        else:
            return True, -1
    return False, None


def max_step(line):
    check = is_over(line, 1)
    if check[0]:
        return check[1]
    results = []
    children = possible_next_strings(line)
    for next_line in children:
        results.append(min_step(next_line[0]))
    return max(results)


def min_step(line):
    check = is_over(line, 2)
    if check[0]:
        return check[1]
    results = []
    children = possible_next_strings(line)
    for next_line in children:
        results.append(max_step(next_line[0]))
    return min(results)


def max_move(line):
    children = possible_next_strings(line)
    winners = []
    for next_line in children:
        value = min_step(next_line[0])
        if value == 1:
            winners.append(next_line[1])
    return winners


def min_move(line):
    children = possible_next_strings(line)
    winners = []
    for next_line in children:
        value = max_step(next_line[0])
        if value == -1:
            winners.append(next_line[1])
    return winners


dictionary = set()
substrings = set()
minimum_length = int(sys.argv[2])
st = ""
if len(sys.argv) == 4:
    st = sys.argv[3]
with open(sys.argv[1]) as f:
    for word in f:
        word = word.strip()
        if len(word) >= minimum_length and word.isalpha():
            dictionary.add(word.upper())
            char = ""
            for x in range(len(word)):
                char += word[x]
                substrings.add(char.upper())
to_win = []
if len(st) % 2 == 0:
    to_win = max_move(st)
else:
    to_win = min_move(st)
if len(to_win) == 0:
    print("Next player will lose!")
else:
    print(f"Next player can guarantee victory by playing any of these letters: {to_win}")


