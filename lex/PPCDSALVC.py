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
    logs = FileStream(argv[2])

    lexer = PPCDSALVCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PPCDSALVCParser(stream)
    err = errores()
    semantica = semantics()
    log = open('logs', 'a')
    parser._listeners = [ myErrorListener(log) ]

    try:
        tree = parser.programa()
    except:
        log.close()

    printer = PPCDSALVCCustomListener(semantica, err)
    walker = ParseTreeWalker()


    try:
        walker.walk(printer, tree)
    except:

        if len(err.errors) > 0:
            for elem in err.errors:
                log.write(elem.msg+"\n")
            log.close()
            sys.exit()


    




    print(len(printer.cuadruplos))
    for quad in printer.cuadruplos:
        quad.imprimirCuadruplo()

    #print("Accepted")

    parsed = (semantica.classes)
    #print (json.dumps(parsed, indent=2))

    log.close()

if __name__ == '__main__':
    main(sys.argv)


