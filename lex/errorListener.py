from antlr4.error.ErrorListener import ErrorListener
import sys


class myErrorListener( ErrorListener):

    def __init__(self,log):
        self.log = log

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.log.write (str(line) + ":" + str(column) + ": sintax ERROR, " + str(msg) + "\n")
        sys.exit(1)

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
