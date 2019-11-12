from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from listener import PPCDSALVCCustomListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics
from errorListener import myErrorListener
from errorListener import errores

import json
import sys
import os
import pprint


def main(argv):
    input = FileStream(argv[1])
    
    if len(argv) > 2:
        logs = str(argv[2])
        DIR = './../../quad/'
    else:
        logs = './../logs/err.txt'
        DIR = './../quad/'


    
    lexer = PPCDSALVCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PPCDSALVCParser(stream)
    err = errores()
    semantica = semantics()
    log = open(logs, 'a')
    log.write("\n")

    parser._listeners = [ myErrorListener(log) ]

    try:
        tree = parser.start()
    except ex:
        print(ex)
        log.write("\n")
        log.close()
        sys.exit(1)

    printer = PPCDSALVCCustomListener(semantica, err)
    walker = ParseTreeWalker()



    try:
        walker.walk(printer, tree)
        semantica.pr()
    except ex:
        print(ex)
        if len(err.errors) > 0:
            for elem in err.errors:
                log.write(elem.msg+"\n")
        log.write("\n")
        log.close()
        sys.exit(1)



    fileName = DIR + "quad_"
    fileName += str(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
    fileName += ".PPCDSALVC"

    for quad in printer.cuadruplos:
        quad.imprimirCuadruplo(fileName)

    #print("Accepted")

     
#    parsed = str(semantica.clases)


    log.close()

if __name__ == '__main__':
    main(sys.argv)


