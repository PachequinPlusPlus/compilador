from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from PPCDSALVCListener import PPCDSALVCListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics
from errorListener import errores
from errorListener import myErrorListener
from cuadruplo import cuadruplo

import sys


#TODO(falta checar cuando se intenta utilizar algo, que exista xdxdd)

class PPCDSALVCCustomListener(PPCDSALVCListener):

    # atr

    #Boleanos
    isClass = False
    isFunction = False

    # ints
    numberParams = 0


    # Strings
    nameFunction = None
    lastType = None
    returnType = None


    # stacks para cuadruplos
    expStack = []
    tipoStack = []
    opStack = []



    def tope(self, stack):
        return stack[len(stack)-1]

    def push(self, stack, val):
        stack.append(val)

    def pop(self, stack):
        stack.pop()

    def enterCte(self, ctx):
        if ctx.INT() is not None:
            val = ctx.INT()
        elif ctx.FLOAT() is not None:
            val = ctx.FLOAT()
        elif ctx.CHAR() is not None:
            val = ctx.CHAR()
        self.push(self.expStack, val)


    
    def enterFactor(self, ctx):
        pass       


    def resolveExp(self, ctx):
        if len(self.opStack) > 0:
            operando = self.tope(self.opStack)
            if operando == '+' or operando == '-':
                self.pop(self.opStack)

                left = self.tope(self.expStack) 
                self.pop(self.expStack)
                right = self.tope(self.expStack) 
                self.pop(self.expStack)

                leftT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)
                rightT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)

                left, right = right, left
                leftT, rightT = rightT, leftT

                resultT = self.semantica.cube[leftT][rightT][operando]
                if resultT != "err":
                    resultAddress = self.semantica.getAddress(resultT, True)
                    self.pushCuadruplo(operando, left, right, resultAddress)
                    self.push(self.expStack, resultAddress)
                    self.push(self.tipoStack, resultT)
                else:
                    self.err.push("type mismatch : "+leftT+" and "+rightT+" | line "+str(ctx.start.line), 403)
                    sys.exit()

    def resolveTerm(self, ctx):
        if len(self.opStack) > 0:
            operando = self.tope(self.opStack)
            if operando == '*' or operando == '/':
                self.pop(self.opStack)

                left = self.tope(self.expStack) 
                self.pop(self.expStack)
                right = self.tope(self.expStack) 
                self.pop(self.expStack)

                leftT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)
                rightT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)

                left, right = right, left
                leftT, rightT = rightT, leftT

                #TODO(TEMPORAL ERROR)
                try:
                    resultT = self.semantica.cube[leftT][rightT][operando]
                except:
                    self.err.push("tmp, err", 404)
                    sys.exit()

                if resultT != "err":
                    resultAddress = self.semantica.getAddress(resultT, True)
                    self.pushCuadruplo(operando, left, right, resultAddress)
                    self.push(self.expStack, resultAddress)
                    self.push(self.tipoStack, resultT)
                else:
                    self.err.push("type mismatch : "+leftT+" and "+rightT+" | line "+str(ctx.start.line), 403)
                    sys.exit()

    condicionales = ['<', '<=', '>', '>=', '==', '!=']

    def resolveSuperExp(self, ctx):
        if len(self.opStack) > 0:
            operando = self.tope(self.opStack)
            if operando in self.condicionales:
                self.pop(self.opStack)

                left = self.tope(self.expStack) 
                self.pop(self.expStack)
                right = self.tope(self.expStack) 
                self.pop(self.expStack)

                leftT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)
                rightT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)

                left, right = right, left
                leftT, rightT = rightT, leftT

                resultT = self.semantica.cube[leftT][rightT][operando]
                if resultT != "err":
                    resultAddress = self.semantica.getAddress(resultT, True)
                    self.pushCuadruplo(operando, left, right, resultAddress)
                    self.push(self.expStack, resultAddress)
                    self.push(self.tipoStack, resultT)
                else:
                    self.err.push("type mismatch : "+leftT+" and "+rightT+" | line "+str(ctx.start.line), 403)
                    sys.exit()

    logical = ['&&', '||']

    def resolveHyperExp(self, ctx):
        if len(self.opStack) > 0:
            operando = self.tope(self.opStack)
            if operando in logical:
                self.pop(self.opStack)

                left = self.tope(self.expStack) 
                self.pop(self.expStack)
                right = self.tope(self.expStack) 
                self.pop(self.expStack)

                leftT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)
                rightT = self.tope(self.tipoStack)
                self.pop(self.tipoStack)

                left, right = right, left
                leftT, rightT = rightT, leftT

                resultT = self.semantica.cube[leftT][rightT][operando]
                if resultT != "err":
                    resultAddress = self.semantica.getAddress(resultT, True)
                    self.pushCuadruplo(operando, left, right, resultAddress)
                    self.push(self.expStack, resultAddress)
                    self.push(self.tipoStack, resultT)
                else:
                    self.err.push("type mismatch : "+leftT+" and "+rightT+" | line "+str(ctx.start.line), 403)
                    sys.exit()




    def imprimeErrores(self):
        for elem in self.err.errors:
            print(elem.msg)



    def exitTermaux(self, ctx):
        self.resolveTerm(ctx)

    def exitTerm(self, ctx):
        self.resolveTerm(ctx)

    def enterParent(self, ctx):
        self.push(self.opStack, '$')

    def exitParent(self, ctx):
        self.pop(self.opStack)

    def enterSuperexpaux(self, ctx):
        print(str(ctx.relationalop().getChild(0)))
        self.push(self.opStack, str(ctx.relationalop().getChild(0)))

    def exitSuperexpaux(self, ctx):
        self.resolveSuperExp(ctx)

    # este deberia dar un resultado booleano, segun yo..?
    # va a regresar int, no?
    def enterHyperexpaux(self, ctx):
        print(str(ctx.logicop().getChild(0)))
        self.push(self.opStack, str(ctx.logicop().getChild(0)))

    def exitHyperexpaux(self, ctx):
        self.resolveHyperExp(ctx)

    def enterFunccall(self, ctx):
        if self.semantica.checkFunctionExists(str(ctx.ID())) == False:
            fToken = ctx.ID()
            self.err.push("\'"+str(fToken)+"\' function not declared | line : "+str(ctx.start.line), 402)

    def enterExpaux(self, ctx):
        self.push(self.opStack, str(ctx.binbasico().getChild(0)))

    def exitExpaux(self, ctx):
        self.resolveExp(ctx)

    def exitExp(self, ctx):
        self.resolveExp(ctx)

    def enterTermaux(self, ctx):
        self.push(self.opStack, str(ctx.bincomplejo().getChild(0)))
        

    def enterFactorclases(self, ctx):
        # func call
        if ctx.PA() is not None:
            if self.semantica.checkFunctionExists(str(ctx.ID(0))) == False:
                fToken = ctx.ID(0)
                self.err.push("\'"+str(fToken)+"\' function not declared | line : "+str(ctx.start.line), 402)
        # variable 
        elif self.isFunction:
            elemento  = self.semantica.deepLookingFunction(self.nameFunction, str(ctx.ID(0)))
            if elemento == None:
                fToken = ctx.ID(0)
                self.err.push("\'"+str(fToken)+"\' is not defined | line : " + str(ctx.start.line), 401)
            else:
                #TODO(FIX)
                #TODO(Cte doesnt have a tipo)
                self.push(self.expStack, ctx.ID(0))
                self.push(self.tipoStack, elemento["tipo"])
         




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

    def pushCuadruplo(self, op, left, right, result):
        self.cuadruplos.append(cuadruplo(op, left, right, result))
    
    def __init__(self, semantica, errores):
        self.semantica = semantica
        self.err = errores
        self.cuadruplos = []


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

    def enterReturntypes(self, ctx):
        if ctx.TYPES() is not None:
            self.returnTypes = str(ctx.TYPES())
        else:
            self.returnTypes = 'void'

    def exitFunctions(self, ctx):
        self.semantica.updateNumberParams(self.nameFunction, self.numberParams)
        self.semantica.updateReturnType(self.nameFunction, self.returnTypes)
        self.numberParams = 0
        self.isFunction = False
        self.semantica.popFuncs()


    def exitParamfirst(self, ctx):
        self.numberParams = self.numberParams + 1
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
            self.insertVar(str(ctx.ID(0)), ctx)
        else:
            self.lastType = str(ctx.ID(0))
            self.insertVar(str(ctx.ID(1)), ctx)

    def exitParams(self, ctx):
        self.numberParams = self.numberParams + 1
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
            self.insertVar(str(ctx.ID(0)), ctx)
        else:
            self.lastType = str(ctx.ID(0))
            self.insertVar(str(ctx.ID(1)), ctx)



            



    def exitTypesvar(self, ctx):
        pass


