#-*- coding: utf-8 -*-

from random import choice, randint

OP = ['+', '*']

VAL = xrange(0, 100)

def gen_unit_test(nb_op):
    global OP
    global VAL
    nb_par_open = 0
    unit_test = list()
    unit_test.append(choice(VAL))
    for op in xrange(nb_op):
        unit_test.append(choice(OP))
        # Randomly open a parenthesis
        if randint(1, 100) % 2 == 0:
            unit_test.append('(')
            nb_par_open += 1
        unit_test.append(choice(VAL))
        # Randomly close a parenthesis
        if randint(1, 100) % 4 == 0 and nb_par_open > 0:
            unit_test.append(')')
            nb_par_open -= 1
    while nb_par_open > 0:
        unit_test.append(')')
        nb_par_open -= 1
    return " ".join(map(lambda x: str(x), unit_test))

unit_tests = list()
oracles = list()
for i in xrange(1000):
    unit_tests.append(gen_unit_test(i % 5))

oracles = map(lambda x: eval(x), unit_tests)

with open("parenthesis_auto.mad", "w") as mad:
    with open("parenthesis_auto.oracle", "w") as oracle:
        for test, ora in zip(unit_tests, oracles):
            mad.write("$(( {0} ))\n".format(test))
            oracle.write("{0}\n".format(ora))

