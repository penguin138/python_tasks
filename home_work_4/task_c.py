#! /usr/bin/env python3
import re
import sys


def main():
    regexp = r'((from [a-z\.]+ )?import [a-z\.]+(, [a-z\.]+)*)'
    imports = []
    matched = re.findall(regexp, sys.stdin.read())
    # print(matched)
    for matched_tuple in matched:
        string = matched_tuple[0]
        parts = re.split('\s+', string)
        if 'from' in string:
            imports.append(parts[1])
            # print(parts[1])
        else:
            for part in parts[1:]:
                if ',' in part:
                    part = part[:-1]
                # print(part)
                imports.append(part)
    print(', '.join(sorted(set(imports))))
main()
