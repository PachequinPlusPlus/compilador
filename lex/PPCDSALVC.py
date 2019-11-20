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
import argparse




def main(argv):
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--logs", help = "path to logs", default="./../logs/err.txt")
    parser.add_argument("--programa", help = "path to program")
    parser.add_argument("--quads", help = "path to quads", default="./../quad/")
    parser.add_argument("--show_quads", help = "if flag is on, show quads", action='store_true')
    parser.add_argument("--show_logs", help = "if flag is on, show logs", action='store_true')

    args = parser.parse_args()




    # input file
    input = FileStream(args.programa)
    # logs path
    logs = args.logs
    # quads path
    DIR = args.quads

    
    lexer = PPCDSALVCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PPCDSALVCParser(stream)
    err = errores()
    semantica = semantics()
    log = open(logs, 'a')
    log.write("\n")

    parser._listeners = [ myErrorListener(log, args.show_logs) ]

    try:
        tree = parser.start()
    except SystemExit:
        log.write("\n")
        log.close()
        sys.exit(1)

    printer = PPCDSALVCCustomListener(semantica, err)
    walker = ParseTreeWalker()



    try:
        walker.walk(printer, tree)
        semantica.pr()
    except SystemExit:
        if len(err.errors) > 0:
            for elem in err.errors:
                if args.show_logs:
                    print(elem.msg)
                log.write(elem.msg+"\n")
        log.write("\n")
        log.close()
        sys.exit(1)



    fileName = DIR + "quad_"
    fileName += str(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
    fileName += ".PPCDSALVC"

    ret = 0
    for quad in printer.cuadruplos:
        quad.imprimirCuadruplo(fileName, ret, args.show_quads)
        ret = ret + 1



    log.close()

if __name__ == '__main__':
    main(sys.argv)


