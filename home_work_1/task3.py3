#!/usr/bin/env python3

def count_letters():
    fin = open("input.txt", 'r')
    letter_dict = {}
    for line in fin:
        line = line.lower()
        for symbol in line:
            if (symbol.isalpha()):
                if (symbol in letter_dict):
                    letter_dict[symbol] += 1
                else:
                    letter_dict[symbol] = 1
    fin.close()
    out = open("output.txt", 'w')
    for item in sorted(letter_dict.items(),key = lambda x: (-x[1],x[0])):
        out.write(item[0] + ": " + str(item[1]) + "\n")
    out.close()
count_letters()
