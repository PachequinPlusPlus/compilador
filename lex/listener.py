from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from PPCDSALVCListener import PPCDSALVCListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics

import sys



class PPCDSALVCCustomListener(PPCDSALVCListener):

    # atr

    #Boleanos
    isClass = False
    isFunction = False



    # Strings
    nameFunction = None
    lastType = None


    def insertVar(self, varName):
        tipo = self.lastType
        if self.isFunction:
            self.semantica.addAttrFunction(self.nameFunction, varName, tipo) 
        else:
            self.semantica.addAttrGlobal(varName, tipo)

    def insertScope(self, scopeStyle, scope):
        pass
        #self.semantica.

    
    def __init__(self, semantica):
        self.semantica = semantica


    def enterPrograma(self, ctx):
        pass

    def exitPrograma(self, ctx):
        pass

    def enterTypesvar(self, ctx):
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
        else:
            print(ctx.ID())
            self.lastType = str(ctx.ID())
        indices = []

        indices.append(str(ctx.typesvaraux().ID()))
        for act in ctx.secondType():
            indices.append(str(act.ID()))

        for vr in indices:
            self.insertVar(vr)


    def exitTypesvar(self, ctx):
        self.semantica.popType()

    def enterMain(self, ctx):
        self.isFunction=True
        self.nameFunction = "main"
        self.semantica.appendFuncs("main")

    def exitMain(self, ctx):
        self.isFunction = False
        self.semantica.popFuncs()

    def enterClasses(self, ctx):
        self.isClass = True
        self.semantica.appendScope(str(ctx.ID(0)))

    def exitClasses(self, ctx):
        self.isClass = False
        self.semantica.popScope()
        if ctx.PP is not None:
            self.semantica.appendParentForClasses(str(ctx.ID(0)), str(ctx.ID(1)))

    def enterFunctions(self, ctx):
        self.isFunction = True
        self.nameFunction = str(ctx.ID())
        self.semantica.appendFuncs(str(ctx.ID()))
        if self.isClass:
            self.semantica.addMethod(str(ctx.ID()))
        else:
            self.semantica.addFunction(str(ctx.ID()))

    def exitFunctions(self, ctx):
        self.isFunction = False
        self.semantica.popFuncs()


    def exitParamfirst(self, ctx):
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
            self.insertVar(str(ctx.ID(0)))
        else:
            self.lastType = str(ctx.ID(0))
            self.insertVar(str(ctx.ID(1)))

    def exitParams(self, ctx):
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
            self.insertVar(str(ctx.ID(0)))
        else:
            self.lastType = str(ctx.ID(0))
            self.insertVar(str(ctx.ID(1)))



            



    def exitTypesvar(self, ctx):
        pass


