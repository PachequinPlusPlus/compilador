from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from PPCDSALVCListener import PPCDSALVCListener
from PPCDSALVCParser import PPCDSALVCParser
import sys


def main(argv):
    input = FileStream(argv[1])
    lexer = PPCDSALVCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PPCDSALVCParser(stream)
    tree = parser.programa()

if __name__ == '__main__':
    main(sys.argv)

