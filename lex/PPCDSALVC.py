from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from PPCDSALVCListener import PPCDSALVCListener
from PPCDSALVCParser import PPCDSALVCParser

import sys


cube = {
        'int' : {
                'int' : {
                        '+' : 'int',
                        '-' : 'int',
                        '/' : 'int',
                        '*' : 'int',
                        '<' : 'int',
                        '>' : 'int',
                        '<=' : 'int',
                        '>=' : 'int',
                        '!=' : 'int',
                        '==' : 'int',
                        '&&' : 'int',
                        '||' : 'int'
                    },
                'float' : {
                        '+' : 'float',
                        '-' : 'float',
                        '/' : 'float',
                        '*' : 'float',
                        '<' : 'int',
                        '>' : 'int',
                        '<=' : 'int',
                        '>=' : 'int',
                        '!=' : 'int',
                        '==' : 'int',
                        '&&' : 'int',
                        '||' : 'int'
                    },
                'char' : {
                        '+' : 'err',
                        '-' : 'err',
                        '/' : 'err',
                        '*' : 'err',
                        '<' : 'err',
                        '>' : 'err',
                        '<=' : 'err',
                        '>=' : 'err',
                        '!=' : 'err',
                        '==' : 'err',
                        '&&' : 'err',
                        '||' : 'err'
                    }
            },
        'float' : {
                'int' : {
                        '+' : 'float',
                        '-' : 'float',
                        '/' : 'float',
                        '*' : 'float',
                        '<' : 'int',
                        '>' : 'int',
                        '<=' : 'int',
                        '>=' : 'int',
                        '!=' : 'int',
                        '==' : 'int',
                        '&&' : 'int',
                        '||' : 'int'
                    },
                'float' : {
                        '+' : 'float',
                        '-' : 'float',
                        '/' : 'float',
                        '*' : 'float',
                        '<' : 'int',
                        '>' : 'int',
                        '<=' : 'int',
                        '>=' : 'int',
                        '!=' : 'int',
                        '==' : 'int',
                        '&&' : 'int',
                        '||' : 'int'
                    },
                'char' : {
                        '+' : 'err',
                        '-' : 'err',
                        '/' : 'err',
                        '*' : 'err',
                        '<' : 'err',
                        '>' : 'err',
                        '<=' : 'err',
                        '>=' : 'err',
                        '!=' : 'err',
                        '==' : 'err',
                        '&&' : 'err',
                        '||' : 'err'
                    }
            },
        'char' : {
                'int' : {
                        '+' : 'err',
                        '-' : 'err',
                        '/' : 'err',
                        '*' : 'err',
                        '<' : 'err',
                        '>' : 'err',
                        '<=' : 'err',
                        '>=' : 'err',
                        '!=' : 'err',
                        '==' : 'err',
                        '&&' : 'err',
                        '||' : 'err'
                    },
                'float' : {
                        '+' : 'err',
                        '-' : 'err',
                        '/' : 'err',
                        '*' : 'err',
                        '<' : 'err',
                        '>' : 'err',
                        '<=' : 'err',
                        '>=' : 'err',
                        '!=' : 'err',
                        '==' : 'err',
                        '&&' : 'err',
                        '||' : 'err'
                    },
                'char' : {
                        '+' : 'err',
                        '-' : 'err',
                        '/' : 'err',
                        '*' : 'err',
                        '<' : 'int',
                        '>' : 'int',
                        '<=' : 'int',
                        '>=' : 'int',
                        '!=' : 'int',
                        '==' : 'int',
                        '&&' : 'err',
                        '||' : 'err'
                    }
            }
}

class PPCDSALVCListener(ParseTreeListener):
    def enterPrograma(self, ctx):
        print("start parsing")

    def exitPrograma(self, ctx):
        print("end parsing")

    def enterTypesvaraux(self, ctx):
        print("types")
        print(ctx.getText())

    def enterSecondType(self, ctx):
        print("secondType")
        print(ctx.getText()[1:])

def main(argv):
    input = FileStream(argv[1])
    lexer = PPCDSALVCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = PPCDSALVCParser(stream)
    tree = parser.programa()

    printer = PPCDSALVCListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main(sys.argv)


