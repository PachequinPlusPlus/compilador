from antlr4.error.ErrorListener import ErrorListener
import sys


class myErrorListener( ErrorListener ):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print (str(line) + ":" + str(column) + ": sintax ERROR, " + str(msg))
        sys.exit()

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception("Oh no!!")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception("Oh no!!")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception("Oh no!!")

class error():
    msg = "",
    errorCode = -1

    def __init__(self, msg, code):
        self.msg = msg
        self.code = code


class errores():
    errors = []
    
    def push(self, msg, code):
        self.errors.append(error(msg, code))
