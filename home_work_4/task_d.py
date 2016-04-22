import argparse
import sys


def tokenize(str):
    tokens = []
    current_token = ""
    for symbol in str:
        if symbol.isdigit() and (current_token.isdigit() or current_token == ""):
            current_token += symbol
        elif symbol.isalpha() and (current_token.isalpha() or current_token == ""):
            current_token += symbol
        elif not symbol.isalpha() and not symbol.isdigit():
            tokens.append(current_token)
            tokens.append(symbol)
            current_token = ""
    return tokens


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('function', type=str,
                        choices=['tokenize', 'probabilities', 'generate', 'test'])
    args = parser.parse_args()
    function = args['function']
    if function == 'tokenize':
        string = sys.stdin.read()
        tokens = tokenize(string)
        for token in tokens:
            print(token)
    else:
        pass
