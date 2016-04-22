#! /usr/bin/env python3
import re
import sys


def main():
    date = '[0-9]{2}'  # date regexp
    month = '[0-9]{2}'  # month regexp
    month_word = '[а-я]+'  # month word regexp
    year = '[0-9]{4}'  # year regexp
    date_2 = '[0-9]{1,2}'  # second date regexp
    delims = ['/', '\.', '\-']  # delimiter 1
    delim2 = '\s*'
    begin = '^'
    end = '$'
    regexes = []
    date_parts = [date, month, year]
    for delim in delims:
        regex = re.compile(begin + delim.join(date_parts) + end)
        regexes.append(regex)
        regex = re.compile(begin + delim.join(reversed(date_parts)) + end)
        regexes.append(regex)
    date_parts_2 = [date_2, month_word, year]
    regexes.append(re.compile(begin + delim2.join(date_parts_2) + end, re.UNICODE))
    for line in sys.stdin:
        match = False
        for regex in regexes:
            if regex.match(line.strip()) is not None:
                print("YES")
                match = True
                break
        if not match:
            print("NO")
main()
