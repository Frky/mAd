#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys

from expr import Expr

class MadParser(object):

    def __init__(self, mad, md=""):
        """
            @param mad   path to the Markdown+a file to parse
            @param md  path to the Markdown output file 
                        (optional) if not provided, output is saved 
                        at the same location as mad

        """
        # TODO check paths
        # (in particular: does mad exist? does md exist? If yes, overwrite?)
        self.__in = mad
        if md == "":
            self.__out = "{0}.{1}".format(os.path.splitext(mad)[0], "md")
        else:
            self.__out = md
        # Dictionnary of variables
        self.__vars = dict()

    def __update_var(self, var, val):
        self.__vars[var] = val

    def __evaluate(self, expr):
        #TODO handle variables
        print "Evaluating {0}".format(expr)
        # For the record: the result of an expression of the form $(( ... )) is printed, 
        # whereas the result of an expression of the form $( ... ) is not
        verbose = False
        if expr[0] == "(":
            if expr[-1] != ")":
                #TODO specific exception
                raise Exception
            verbose = True
            expr = expr[1:-1]
        res = Expr(expr).eval()
        if verbose:
            return str(res)
        else:
            return ""

    def parse(self):
        #TODO god this is ugly...
        with open(self.__in, "r") as in_file:
            with open(self.__out, "w") as out_file:
                expr = ""
                c = in_file.read(1)
                while c:
                    print c
                    if c == "$":
                        print "$"
                        # Read next char
                        c = in_file.read(1)
                        if c == "(":
                            # Number of new parenthesis to close
                            nb_open = 0
                            # Beginning of an expression
                            c = in_file.read(1)
                            while c != ")" or nb_open != 0:
                                if c == "(":
                                    nb_open += 1
                                elif c == ")":
                                    nb_open -= 1
                                #TODO error if nb_open is negative
                                expr += c
                                c = in_file.read(1)
                            out_file.write(self.__evaluate(expr))
                            expr = ""
                        else:
                            # Write forgotten char
                            out_file.write("$")
                    else:
                        out_file.write(c)
                    c = in_file.read(1)


if __name__ == "__main__":
    madparser = MadParser(sys.argv[1])
    madparser.parse()

