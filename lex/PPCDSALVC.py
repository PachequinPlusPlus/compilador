from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from listener import PPCDSALVCCustomListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics
from errorListener import myErrorListener
from errorListener import errores

import json
import mappingQuads
import pickle
import sys
import os
import pprint
import argparse




def main(argv):
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--logs", help = "path to logs", default="./../logs/err.txt")
    parser.add_argument("--programa", help = "path to program")
    parser.add_argument("--quads", help = "path to quads", default="./../quad/")
    parser.add_argument("--quad_file", help = "specify the quad file name to generate")
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
    fileTemp = str(args.quad_file).split('/')
    fileName += fileTemp[len(fileTemp) -1] + "_"
    fileName2 = fileName + "a"
    fileName += ".PPCDSALVC"
    fileName2 += ".PPCDSALVC"


    ret = 0
    quadFile = open(fileName, 'wb')
    quadFile2 = open(fileName2, 'w')
    quads = []
    for quad in printer.cuadruplos:
        quad.imprimirCuadruplo(fileName, ret, args.show_quads)
        ret = ret + 1
        maped = False
        for i in range(len(mappingQuads.mapQuadsList)):
            if mappingQuads.mapQuadsList[i] == quad.op:
                aux = quad
                aux.op = i
                quads.append([aux.op, aux.left, aux.right, aux.result])
                quadFile2.write(str([aux.op, aux.left, aux.right, aux.result]) + "\n")
                maped = True
                break
        if maped == False:
            print(quad.op + " is not defined")
            log.write(quad.op+" is not defined\n")
            log.write("\n")
            log.close()
            sys.exit(1)


    pickle.dump(quads, quadFile)
    quadFile2.close()
    quadFile.close()

    log.close()

if __name__ == '__main__':
    main(sys.argv)


