import math


def multiply(values):
    total = 1
    for value in values:
        total *= value
    return math.sqrt(total)
