from math import cos


def calc(a, b, operator):
    if operator == '+':
        return cos(a)
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b