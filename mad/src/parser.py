#-*- coding: utf-8 -*-

import os

from ast.expr import Expr

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
        # For the record: the result of an expression of the form $(( ... )) is printed, 
        # whereas the result of an expression of the form $( ... ) is not
        verbose = False
        if expr[0] == "(":
            if expr[-1] != ")":
                #TODO specific exception
                raise Exception
            verbose = True
            expr = expr[1:-1]
        # Variable definition?
        if expr.count("=") == 1:
            # Get variable name and value
            var, expr = expr.split("=")
            # Filter variable name
            var = var.replace(" ", "")
            # TODO
            # Perform verifications on variable name
            # ...
            # Compute value 
            val = Expr(expr, self.__vars).eval()
            # Assign value to variable
            self.__vars[var] = val
        # If more than one "=": syntax error
        elif expr.count("=") > 1:
            # TODO explicit error
            raise Exception
        else:
            val = Expr(expr, self.__vars).eval()
        if verbose:
            return str(val)
        else:
            return ""

    def parse(self):
        #TODO god this is ugly...
        with open(self.__in, "r") as in_file:
            with open(self.__out, "w") as out_file:
                expr = ""
                c = in_file.read(1)
                while c:
                    if c == "$":
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
