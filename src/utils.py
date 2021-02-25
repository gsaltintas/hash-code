import math


def gcd(args:list):
    res = args[0]
    for num in args[1:]:
        res = math.gcd(res, num)
    return res