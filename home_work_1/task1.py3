#!/usr/bin/env python3

def fibonacci(n):
    if (n < 2):
        print(n)
        return
    prev1 = 0
    prev2 = 1
    result = 0
    for i in range(2,n + 1):
        result = prev1 + prev2
        prev1 = prev2
        prev2 = result
    print(result)
fibonacci(int(input()))
