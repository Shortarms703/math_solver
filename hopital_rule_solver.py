import math
from math_classes import *


# -------------------------
# PROBABLY ALL BROKEN
# -------------------------

def solver(lim, equation):
    steps = []
    lim = '0'
    equation = '(e^(2t)-1)/sin(t)'



    return steps

    # steps = []
    # steps.append(r'\lim_{x \to 0}\frac{\sin{x}}{x}')
    # steps.append(r'''
    #         \lim_{x \to 0}
    #         \frac
    #         {\frac{d}{dx}\left( \sin{x} \right)}
    #         {\frac{d}{dx}\left( {x} \right)}''')
    # steps.append(r'''
    #         \lim_{x \to 0}
    #         \frac{\cos{x}}{1}''')
    # steps.append('1')


def bracket_span(section, brackets='{}'):
    OPEN = brackets[0]
    CLOSE = brackets[1]
    total_open = 0
    for location, ch in enumerate(section):
        if ch == OPEN:
            total_open += 1
        if ch == CLOSE:
            total_open -= 1
        if total_open == 0:
            return location


def split_latex_equation(equation):
    section = equation
    final = Expression(section) # not fully defined expression
    while not final.fully_defined():
        for n in range(len(section)):
            if section[n:n+5] == '\\frac':
                section = section[n+5:]
                location = bracket_span(section)
                numerator = section[1:location]

                section = section[location + 1:]
                location = bracket_span(section)
                denominator = section[1:location]

                final += [Fraction(numerator, denominator)]
                section = equation

            if section[n] == '^':
                section = section[n:]
    return final


# print(split_latex_equation(r'\frac{e^{2x}-1}{\sin(x)}\frac{1}{1}'))
