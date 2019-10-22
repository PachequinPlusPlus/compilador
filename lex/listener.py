from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from PPCDSALVCListener import PPCDSALVCListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics

import sys



class PPCDSALVCCustomListener(PPCDSALVCListener):

    def __init__(self, semantica):
        self.semantica = semantica


    def enterPrograma(self, ctx):
        pass
        #print("start parsing")

    def exitPrograma(self, ctx):
        pass
#        print("end parsing")

    def enterTypesvar(self, ctx):
       # if ctx.TYPES() is None:
            #cuando es clase
            #print(ctx.ID())
       # else:
            #cuando es tipo
#            print(ctx.TYPES());

#        print(ctx.typesvaraux().ID())
        self.semantica.appendVariable(str(ctx.typesvaraux().ID()))

        for act in ctx.secondType():
#            print(act.ID())
            self.semantica.appendVariable(str(act.ID()))

    def enterMain(self, ctx):
        self.semantica.appendFuncs("main")

    def exitMain(self, ctx):
        self.semantica.popFuncs()

    def enterClasses(self, ctx):
        self.semantica.appendScope(str(ctx.ID(0)))

    def exitClasses(self, ctx):
        self.semantica.popScope()

    def enterFunctions(self, ctx):
        self.semantica.appendFuncs(str(ctx.ID()))

    def exitFunctions(self, ctx):
        self.semantica.popFuncs()

    def exitTypesvar(self, ctx):
        pass


