#!/usr/bin/env python3
import string
import sys
from os import listdir, stat
from os.path import join, isfile
def taskOne(n):
    print [(x,y,z) for x in range(n)
            for y in range(x,n) for z in range(max(x,y),n) if (x**2 + y**2 == z**2)]
taskOne(6)
def taskTwo():
    dictionary = {}
    f = open("input.txt",'r')
    for line in f:
        [word,definitions]=line.split(" - ");
        for defin in definitions.split():
            defin = defin.strip()
            if (defin[len(defin) - 1] in string.punctuation):
                defin = defin[0:len(defin) - 1]
            if (defin in dictionary):
                dictionary[defin].add(word)
            else:
                dictionary[defin]=set([word])
    #out = open("output.txt",'w')
    #for key, value in sorted(dictionary.items()):
    #        out.write(key + " - " + ' '.join(list(value)+"\n"))
    print sorted(dictionary.items())
    f.close()
    #out.close()
taskTwo()
def taskThree():
    path = sys.argv[1]
    files = [entry for entry in listdir(path) if (isfile(join(path,entry)))]
    withSizes = {}
    for f in files:
        withSizes[f]= -stat(join(path,f)).st_size
    for  f, size in sorted(withSizes.items(),key = lambda x : (x[1],x[0])):
        print(f + " " + str(abs(size)))

taskThree()
def taskFour():
    pi = open("pi.txt",'r')
    piStr = pi.read()
    substr = sys.stdin.read()
    numberOfOccurenses = string.count(piStr,substr)
    prevStr = piStr
    occurenses = []
    for i in range(5):
        occurenses.append()
