#! /usr/bin/env python3
import argparse
import sys
import random
import unittest
from collections import defaultdict


class TextGenerator(object):

    def __init__(self, text="", max_depth=2):
        self.text_tokens = []
        for line in text:
            self.text_tokens.append(self.tokenize(line))
        self.max_depth = max_depth

    def tokenize(self, str):
        tokens = []
        current_token = ""
        for symbol in str:
            if symbol.isdigit() and (current_token.isdigit() or current_token == ""):
                current_token += symbol
            elif symbol.isalpha() and (current_token.isalpha() or current_token == ""):
                current_token += symbol
            elif not symbol.isalpha() and not symbol.isdigit():
                if current_token != "":
                    tokens.append(current_token)
                tokens.append(symbol)
                current_token = ""
            else:
                tokens.append(current_token)
                current_token = symbol
        if current_token != "":
            tokens.append(current_token)
        return tokens

    def print_tokens(self, tokens):
        for token in tokens:
            print(token)

    def add_token(self, chain, token):
        curr_tuple = tuple(chain)
        if curr_tuple != () and len(token) > 0:
            self.probabilities[curr_tuple][token] += 1

    def _init_chains(self, line_length):
        current_chains = []
        for depth in range(self.max_depth + 1):
            current_chains.append([0, depth])
        return current_chains

    def compute_probabilities(self, only_words=True, line_history=True, only_freqs=False):
        # count token frequencies
        self.probabilities = defaultdict(lambda: defaultdict(int))
        current_chains = []
        if not line_history:
            self.text_tokens = [[x for item in self.text_tokens for x in item]]
        for line in self.text_tokens:
            if only_words:
                line = [token for token in line if token.isalpha()]
            current_chains = self._init_chains(len(line))
            reached_end = False
            while not reached_end:
                for chain_idx in range(len(current_chains)):
                    chain = current_chains[chain_idx]
                    left, right = chain
                    if right < len(line):
                        chain_tokens = line[left: right]
                        next_token = line[right]
                        if left == right:
                            chain_tokens = [""]
                            next_token = line[left]
                        self.add_token(chain_tokens, next_token)
                        current_chains[chain_idx] = [left + 1, right + 1]
                    elif chain_idx == 0:  # the end of zero-length window reached end of line
                        reached_end = True
        # make probabilities out of frequencies
        if not only_freqs:
            for token_seq in self.probabilities.keys():
                all_tokens = 0
                probs = self.probabilities[token_seq]
                for token in probs.keys():
                    all_tokens += probs[token]
                for token in probs.keys():
                    probs[token] /= float(all_tokens)

    def print_probabilities(self):
        sorted_probabilities = sorted(self.probabilities.items())
        for chain, probabilities in sorted_probabilities:
            print(" ".join(chain))
            for token, token_prob in sorted(probabilities.items()):
                print("  {}: {:.2f}".format(token, float(token_prob)))

    def _get_random_object(self, objects, distribution):
        num_of_objects = len(objects)
        if len(distribution) != num_of_objects:
            raise ValueError("""Distribution should consist of {}
                             probabilities - one for each object type""".
                             format(num_of_objects))
        # elif sum(distribution) != 1:
        #    raise ValueError("Sum of p_i should be equal 1")
        random_number = random.random()
        left_sum = 0
        right_sum = 0
        for i in range(num_of_objects):
            right_sum += distribution[i]
            if (random_number >= left_sum and random_number < right_sum):
                return objects[i]
            left_sum = right_sum
        # because it happens with zero probability it doesn't matter what to return
        return objects[0]

    def generate(self, size):
        generated = []
        window = [0, 0]
        while len([token for token in generated if token.isalpha()]) < size:
            left, right = window
            chain = generated[left: right]
            while tuple(chain) not in self.probabilities and left <= right:
                left += 1
                chain = generated[left: right]
            if left == right or tuple(chain) not in self.probabilities:
                chain = [""]
            chain_probs = self.probabilities[tuple(chain)]
            objects = list(chain_probs.keys())
            distribution = [chain_probs[obj] for obj in objects]
            next_token = self._get_random_object(objects, distribution)
            generated.append(next_token)
            if len(generated) < self.max_depth:
                window = [0, right + 1]
            else:
                new_left = window[0] + 1
                new_right = window[1] + 1
                window = [new_left, new_right]
        self.generated_text = "".join(generated)
        return generated

    def print_generated_text(self, filename=None):
        if filename:
            with open(filename, 'w') as out_file:
                out_file.write(self.generated_text)
        else:
            print(self.generated_text)


class TestTextGenerator(unittest.TestCase):

    def setUp(self):
        self.text = ["Harry Potter was a highly unusual boy in many ways.",
                     """Extremely unusual though he was, at that moment Harry Potter felt just
like everyone else -- glad, for the first time in his life, that it was
his birthday."""]
        self.generator = TextGenerator(self.text, max_depth=2)

    def test_tokenize(self):
        tokens = self.generator.tokenize(self.text[0])
        self.assertEqual(len(tokens), 20)

    def test_tokenize_2(self):
        tokens = self.generator.tokenize(self.text[0])
        true_tokens = ['Harry', ' ', 'Potter', ' ', 'was', ' ', 'a', ' ', 'highly', ' ', 'unusual',
                       ' ', 'boy', ' ', 'in', ' ', 'many', ' ', 'ways', '.']
        self.assertEqual(tokens, true_tokens)

    def test_probabilities(self):
        self.generator.compute_probabilities(only_words=True)
        probs = self.generator.probabilities[('Harry',)]
        true_probs = {'Potter': 1.0}
        self.assertEqual(probs, true_probs)

    def test_probabilities_2(self):
        self.generator.compute_probabilities(only_words=True)
        probs = self.generator.probabilities
        for chain, tokens in probs.items():
            self.assertLess(sum(tokens.values()) - 1.0, 1e-10)

    def test_frequencies(self):
        self.generator.compute_probabilities(only_words=True, only_freqs=True)
        freqs = self.generator.probabilities[('Harry', 'Potter')]
        true_freqs = {'was': 1, 'felt': 1}
        self.assertEqual(freqs, true_freqs)

    def test_generate(self):
        self.generator.compute_probabilities(only_words=True)
        generated_text = self.generator.generate(3)
        self.assertEqual(len(generated_text), 3)


def exec_tokenize(args):
    string = input()
    generator = TextGenerator()
    tokens = generator.tokenize(string)
    generator.print_tokens(tokens)


def exec_probs(args):
    text = []
    for line in sys.stdin:
        text.append(line)
    generator = TextGenerator(text, args.depth)
    generator.compute_probabilities()
    generator.print_probabilities()


def exec_generate(args):
    text = []
    if args.file:
        f = open(args.file, 'r')
        for line in f:
            text.append(line)
    else:
        for line in sys.stdin:
            text.append(line)
    generator = TextGenerator(text, args.depth)
    generator.compute_probabilities(only_words=False, line_history=False)
    generator.generate(args.size)
    generator.print_generated_text()


def exec_tests(args):
    unittest.main()


def main():
    """ asd. """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    tokenize_parser = subparsers.add_parser('tokenize')
    test_parser = subparsers.add_parser('test')
    probabilities_parser = subparsers.add_parser('probabilities')
    generate_parser = subparsers.add_parser('generate')

    tokenize_parser.set_defaults(function=exec_tokenize)
    test_parser.set_defaults(function=exec_tests)
    probabilities_parser.add_argument('-d', '--depth', type=int, default=1)
    probabilities_parser.set_defaults(function=exec_probs)
    generate_parser.add_argument('-d', '--depth', type=int, default=1)
    generate_parser.add_argument('-s', '--size', type=int, default=2)
    generate_parser.add_argument('-f', '--file', type=str)
    generate_parser.set_defaults(function=exec_generate)
    args = parser.parse_args(input().split())
    args.function(args)

if __name__ == "__main__":
    main()
