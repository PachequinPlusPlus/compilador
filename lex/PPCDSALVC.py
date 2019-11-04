from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from listener import PPCDSALVCCustomListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics
from errorListener import myErrorListener
from errorListener import errores

import json
import sys



def main(argv):
    input = FileStream(argv[1])
    lexer = PPCDSALVCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PPCDSALVCParser(stream)
    err = errores()
    semantica = semantics()
    parser._listeners = [ myErrorListener() ]
    tree = parser.programa()

    printer = PPCDSALVCCustomListener(semantica, err)
    walker = ParseTreeWalker()

    walker.walk(printer, tree)

    if len(err.errors) > 0:
        for elem in err.errors:
            print(elem.msg)
        sys.exit()

    print("Accepted")

    parsed = (semantica.classes)
    print (json.dumps(parsed, indent=2))

if __name__ == '__main__':
    main(sys.argv)


