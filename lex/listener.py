from antlr4 import *
from PPCDSALVCLexer import PPCDSALVCLexer
from PPCDSALVCListener import PPCDSALVCListener
from PPCDSALVCParser import PPCDSALVCParser
from semantic import semantics
from errorListener import errores
from errorListener import myErrorListener
from cuadruplo import cuadruplo
from variable import variable
from clases import clase
from funcion import funcion

import sys


#TODO(falta checar cuando se intenta utilizar algo, que exista xdxdd)

class PPCDSALVCCustomListener(PPCDSALVCListener):

    # atr

    #Boleanos
    isClass = False
    isFunction = False
    isParameter = False
    isPublic = True

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
    jmpStack = []


    # stack para clases y funciones
    classStack = []
    funcStack = []


    def enterPv(self, ctx):
        self.isPublic = False
    
    def exitPv(self, ctx):
        self.isPublic = True

    def exitCondition(self, ctx):
        expType = self.tope(self.tipoStack)
        print(expType)
        if expType != 'int':
            #TODO("mark error")
            print("err")
        else:
            result = self.tope(self.expStack)
            self.pushCuadruplo('gotof', result , None, -1)
            self.push(self.jmpStack, len(self.cuadruplos)-1)

    def exitconditionSecond(self, ctx):
        jmp = self.tope(self.jmpStack)
        self.pop(self.jmpStack)
        self.cuadruplos[jmp].result = len(self.cuadruplos)

        

    def enterClasses(self, ctx):
        self.isClass = True
        name = str(ctx.ID(0))
        if ctx.PP() is not None:
            parent = str(ctx.ID(1))
            self.push(self.classStack, self.semantica.addClass(name, parent))
            #self.semantica.appendParentForClasses(str(ctx.ID(0)), str(ctx.ID(1)))
        else:
            self.push(self.classStack, self.semantica.addClass(name, "global"))
#            self.semantica.appendParentForClasses(str(ctx.ID(0)), "global")

    def exitClasses(self, ctx):
        self.isClass = False
        self.pop(self.classStack)

    def enterPrograma(self, ctx):
        self.push(self.classStack, self.semantica.addClass("global", None))



    def __init__(self, semantica, errores):
        self.semantica = semantica
        self.err = errores
        self.cuadruplos = []

       # self.semantica.addClass("global", None)

    def enterParameters(self, ctx):
        self.isParameter = True

    def exitParameters(self, ctx):
        self.isParameter = False

    
    def exitAssignment(self, ctx):
        if ctx.IGUAL() is not None:
            self.pushCuadruplo('=', None , self.tope(self.expStack), str(ctx.ID()))
            self.pop(self.expStack)

    
    def insertVar(self, varName, ctx, isArray = False):
       tipo = self.lastType
        
       if self.isFunction:
           if self.isParameter:
               self.semantica.addParameter(self.tope(self.funcStack), varName, tipo, -1, False)
           else:
               self.semantica.addVarFunc(self.tope(self.funcStack), varName, tipo, -1, isArray)
       else:
           topeClase = self.tope(self.classStack)
           #TODO(arreglar isArray)
           self.semantica.addAtributo(self.tope(self.classStack), varName, tipo, -1, isArray, self.isPublic)


        #TODO(check for existence)
       return
        #checking for existed variable
   # if self.isFunction:
        #check in the actual scope and global
  #      if self.semantica.existInFunction(self.nameFunction, varName):
            #throe error
  #          fToken = ctx.start
  #          self.err.push("\'"+varName+"\'" + " redefinition | line : " + str(fToken.line), 400)
          #  return
#    else:
        #check in wherever we are
#        if self.semantica.exists(varName):
#            fToken = ctx.start
#            self.err.push("\'"+varName+"\'" + " redefinition | line : " + str(fToken.line), 400)
#            return

#    if self.isFunction:
#        self.semantica.addAttrFunction(self.nameFunction, varName, tipo) 
#    else:
#        self.semantica.addAttrGlobal(varName, tipo)



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
            if operando in self.logical:
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
        self.push(self.opStack, str(ctx.relationalop().getChild(0)))

    def exitSuperexpaux(self, ctx):
        self.resolveSuperExp(ctx)

    # este deberia dar un resultado booleano, segun yo..?
    # va a regresar int, no?
    def enterHyperexpaux(self, ctx):
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
            if self.semantica.checkFunctionExists(self.tope(self.classStack), str(ctx.ID(0))) == False:
                fToken = ctx.ID(0)
                self.err.push("\'"+str(fToken)+"\' function not declared | line : "+str(ctx.start.line), 402)
        # variable 
        else:
            elemento  = self.semantica.existVariable(self.tope(self.classStack), self.tope(self.funcStack).name, str(ctx.ID(0)))
            if elemento == None:
                fToken = ctx.ID(0)
                self.err.push("\'"+str(fToken)+"\' is not defined | line : " + str(ctx.start.line), 401)
            else:
                #TODO(FIX)
                #TODO(Cte doesnt have a tipo)
                self.push(self.expStack, ctx.ID(0))
                self.push(self.tipoStack, elemento.tipo)
     




    def insertScope(self, scopeStyle, scope):
        pass
        #self.semantica.

    def pushCuadruplo(self, op, left, right, result):
        self.cuadruplos.append(cuadruplo(op, left, right, result))

    def enterTypesvar(self, ctx):
        sonArreglos = []
        if ctx.TYPES() is not None:
            self.lastType = str(ctx.TYPES())
        else:
            self.lastType = str(ctx.ID())
        indices = []

        indices.append(str(ctx.typesvaraux().ID()))
        if ctx.typesvaraux().LB() is not None:
            sonArreglos.append(True)
        else:
            sonArreglos.append(False)
                
        for act in ctx.secondType():
            indices.append(str(act.ID()))
            if act.LB() is not None:
                sonArreglos.append(True)
            else:
                sonArreglos.append(False)


        while len(indices) > 0 :
            vr = self.tope(indices)
            self.pop(indices)
            self.insertVar(vr, ctx, self.tope(sonArreglos))
            self.pop(sonArreglos)
            



    def enterMain(self, ctx):
        self.isFunction=True
        self.push(self.funcStack, funcion('main', 'void'))
        self.push(self.funcStack, self.semantica.addFunction(self.tope(self.classStack), True, 'main', 'void'))

        #        self.semantica.appendFuncs("main")

    def exitMain(self, ctx):
        self.isFunction = False
        self.pop(self.funcStack)

    def enterFunctions(self, ctx):
        self.isFunction = True
        nameFunction = str(ctx.ID())
        returnType = str(ctx.returntypes().getChild(0))
        self.push(self.funcStack, self.semantica.addFunction(self.tope(self.classStack), self.isPublic, nameFunction, returnType))

    def exitFunctions(self, ctx):
        self.isFunction = False
        self.pop(self.funcStack)



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


