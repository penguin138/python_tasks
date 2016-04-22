#!/usr/bin/env python3
from math import fabs,pow
def p_norm(p,v):
    result = 0
    for coord in v:
        result += fabs(coord)**p
    print(pow(result,1/p))
p_norm(float(input()),map(lambda x: float(x),input().split()))
