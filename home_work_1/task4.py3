#!/usr/bin/env python3

def new_lines():
    fin = open("input.txt",'r')
    out = open("output.txt",'w')
    max_len = 0
    first = True
    for line in fin:
        if (first):
            max_len = int(line)
            first = False
        else:
            if (len(line) <= max_len):
                out.write(line)
            else:
                words = line.split()
                current_line = ""
                current_line_len = 0
                wrote = False
                for word in words:
                    wrote = False
                    if (current_line_len + len(word) + 1 <= max_len or
                    (current_line_len == 0 and len(word) <= max_len)):
                        if (current_line_len > 0):
                            current_line = current_line + " " + word
                        else:
                            current_line = word
                        current_line_len = len(current_line)
                    else:
                        wrote = True
                        out.write(current_line + "\n")
                        current_line = word
                        current_line_len = len(word)
                if (not wrote or current_line_len > 0):
                    out.write(current_line + "\n")
    fin.close()
    out.close()

new_lines()
