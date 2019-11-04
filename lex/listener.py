from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from PPCDSALVCListener import PPCDSALVCListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics
from errorListener import errores
from errorListener import myErrorListener

import sys



class PPCDSALVCCustomListener(PPCDSALVCListener):

    # atr

    #Boleanos
    isClass = False
    isFunction = False



    # Strings
    nameFunction = None
    lastType = None


    

    def insertVar(self, varName, ctx):
        tipo = self.lastType
        #checking for existed variable
        if self.isFunction:
            #check in the actual scope and global
            if self.semantica.existInFunction(self.nameFunction, varName):
                #throe error
                fToken = ctx.start
                self.err.push("\'"+varName+"\'" + " redefinition | line : " + str(fToken.line), 400)
                return
        else:
            #check in wherever we are
            if self.semantica.exists(varName):
                fToken = ctx.start
                self.err.push("\'"+varName+"\'" + " redefinition | line : " + str(fToken.line), 400)
                return

    



        if self.isFunction:
            self.semantica.addAttrFunction(self.nameFunction, varName, tipo) 
        else:
            self.semantica.addAttrGlobal(varName, tipo)

    def insertScope(self, scopeStyle, scope):
        pass
        #self.semantica.

    
    def __init__(self, semantica, errores):
        self.semantica = semantica
        self.err = errores


    def enterPrograma(self, ctx):
        pass

    def exitPrograma(self, ctx):
        pass

    def enterTypesvar(self, ctx):
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
        else:
            self.lastType = str(ctx.ID())
        indices = []

        indices.append(str(ctx.typesvaraux().ID()))
        for act in ctx.secondType():
            indices.append(str(act.ID()))

        for vr in indices:
            self.insertVar(vr, ctx)


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
        if ctx.PP() is not None:
            self.semantica.appendParentForClasses(str(ctx.ID(0)), str(ctx.ID(1)))
        else:
            self.semantica.appendParentForClasses(str(ctx.ID(0)), "global")

    def exitClasses(self, ctx):
        self.isClass = False
        self.semantica.popScope()

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
            self.insertVar(str(ctx.ID(0)), ctx)
        else:
            self.lastType = str(ctx.ID(0))
            self.insertVar(str(ctx.ID(1)), ctx)

    def exitParams(self, ctx):
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
            self.insertVar(str(ctx.ID(0)), ctx)
        else:
            self.lastType = str(ctx.ID(0))
            self.insertVar(str(ctx.ID(1)), ctx)



            



    def exitTypesvar(self, ctx):
        pass


