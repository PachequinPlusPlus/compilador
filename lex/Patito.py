from antlr4 import *
from PatitoLexer import PatitoLexer
from PatitoListener import PatitoListener
from PatitoParser import PatitoParser
import sys


def main(argv):
    input = FileStream(argv[1])
    lexer = PatitoLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PatitoParser(stream)
    tree = parser.programa()

if __name__ == '__main__':
    main(sys.argv)

