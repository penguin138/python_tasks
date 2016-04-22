#! /usr/bin/env/ python3

import argparse
import sys


class ASCII_Magick(object):

    def __init__(self, image):
        self.height = len(image)
        self.width = 0
        if (self.height > 0):
            self.width = len(image[0])
        self.symbols = "@%#*+=-:. "
        self.symbols_dict = {}
        for i in range(len(self.symbols)):
            self.symbols_dict[self.symbols[i]] = i
        self.image = self.encode(image)

    def encode(self, image):
        encoded_image = []
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(self.symbols_dict[image[i][j]])
            encoded_image.append(new_line)
        return encoded_image

    def print_image(self):
        for i in range(self.height):
            for j in range(self.width):
                symbol = self.symbols[self.image[i][j]]
                print(symbol, end='')
            print()

    def crop(self, left, right, top, bottom):
        new_image = []
        if left < 0:
            left = 0
        if right < 0:
            right = 0
        if top < 0:
            top = 0
        if bottom < 0:
            bottom = 0
        for i in range(top, self.height - bottom):
            new_line = []
            for j in range(left, self.width - right):
                new_line.append(self.image[i][j])
            new_image.append(new_line)
        self.image = new_image
        self.height -= top + bottom
        if (self.height < 0):
            self.height = 0
        self.width -= left + right
        if (self.width < 0):
            self.width = 0

    def expose(self, brightness_amount):
        for i in range(self.height):
            for j in range(self.width):
                self.image[i][j] += brightness_amount
                if self.image[i][j] < 0:
                    self.image[i][j] = 0
                if self.image[i][j] > 9:
                    self.image[i][j] = 9

    def _one_rotation(self, clockwise):
        # transpose
        new_image = [[0 for i in range(self.height)] for j in range(self.width)]
        for i in range(self.height):
            for j in range(self.width):
                new_image[j][i] = self.image[i][j]
        # reverse
        if clockwise:
            for j in range(self.width):
                new_image[j] = list(reversed(new_image[j]))
        else:
            new_image = list(reversed(new_image))
        self.image = new_image
        self.height = len(self.image)
        self.width = 0
        if (self.height > 0):
            self.width = len(self.image[0])

    def rotate(self, angle):
        if angle % 90 != 0:
            raise ValueError("Unsupported angle.")
        num_of_rotations = int(abs(angle) / 90) % 4
        clockwise = (angle < 0)
        for i in range(num_of_rotations):
            self._one_rotation(clockwise)


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('function', help='crop, rotate or expose')
    parser.add_argument('-l', '--left', type=int, default=0)
    parser.add_argument('-r', '--right', type=int, default=0)
    parser.add_argument('-t', '--top', type=int, default=0)
    parser.add_argument('-b', '--bottom', type=int, default=0)
    parser.add_argument('required_value', type=int, nargs='?')
    args = parser.parse_args(input().split())
    image = []
    for line in sys.stdin:
        new_line = []
        for symbol in line:
            if symbol != '\n':
                new_line.append(symbol)
        image.append(new_line)
    magick = ASCII_Magick(image)
    if args.function == 'crop':
        magick.crop(args.left, args.right, args.top, args.bottom)
        magick.print_image()
    elif args.function == 'rotate':
        if args.required_value is None:
            print("Missing argument: angle")
        else:
            magick.rotate(args.required_value)
            magick.print_image()
    elif args.function == 'expose':
        if args.required_value is None:
            print("Missing argument: brightness amount")
        else:
            magick.expose(args.required_value)
            magick.print_image()
    else:
        print('Unknown function.')

start()
