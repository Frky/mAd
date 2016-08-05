#-*- coding: utf-8 -*-

from random import choice

OP = ['+', '*']

VAL = xrange(0, 100)

def gen_unit_test(nb_op):
    global OP
    global VAL
    unit_test = list()
    unit_test.append(choice(VAL))
    for op in xrange(nb_op):
        unit_test.append(choice(OP))
        unit_test.append(choice(VAL))
    return " ".join(map(lambda x: str(x), unit_test))

unit_tests = list()
oracles = list()
for i in xrange(1000):
    unit_tests.append(gen_unit_test(i % 5))

oracles = map(lambda x: eval(x), unit_tests)

with open("add_mul_auto.mad", "w") as mad:
    with open("add_mul_auto.oracle", "w") as oracle:
        for test, ora in zip(unit_tests, oracles):
            mad.write("$(( {0} ))\n".format(test))
            oracle.write("{0}\n".format(ora))

