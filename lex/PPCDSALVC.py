from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from listener import PPCDSALVCCustomListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics

import json
import sys





def main(argv):
    input = FileStream(argv[1])
    lexer = PPCDSALVCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PPCDSALVCParser(stream)
    semantica = semantics()
    tree = parser.programa()

    printer = PPCDSALVCCustomListener(semantica)
    walker = ParseTreeWalker()

    walker.walk(printer, tree)

    parsed = (semantica.classes)
    print (json.dumps(parsed, indent=2))

if __name__ == '__main__':
    main(sys.argv)


