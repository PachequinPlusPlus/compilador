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
    mClass = None




    # stacks para cuadruplos
    expStack = []
    tipoStack = []
    opStack = []
    jmpStack = []

    parameters = []
    tipos = []

    methodStack = []


    # stack para clases y funciones
    classStack = []
    funcStack = []


    def exitMcall(self, ctx):
        if self.semantica.checkFunctionExists(self.semantica.getClase(self.mClass), str(ctx.ID())) == False:
            fToken = ctx.ID()
            self.err.push("\'"+str(fToken)+"\' function not declared | line : "+str(ctx.start.line), 402)
            sys.exit(1)
        else:
            myFunc = self.semantica.getFunc(self.semantica.getClase(self.mClass),  str(ctx.ID()))
            if self.compareFunctions(myFunc) == False:
                self.pushError(str(ctx.ID()), "the function doesnt not match", ctx.start.line, 409)
                sys.exit(1)

            self.push(self.expStack, myFunc.getReturnDir())
            self.push(self.tipoStack, myFunc.tipoRetorno)




    def enterMethod(self, ctx):
        if ctx.mcall() is not None:
            self.push(self.methodStack, str(ctx.ID()))
            #do something
            myVar = self.semantica.existVariable(self.tope(self.classStack), self.tope(self.funcStack).name, self.methodStack[0])
            if myVar is None:
                self.pushError(self.methodStack[0], "var is not defined", ctx.start.line, 401)
                sys.exit(1)
            for i in range(len(self.methodStack)-1):
                myVar = self.semantica.existInClass(self.semantica.getClase(myVar.tipo), self.methodStack[i+1])
                if myVar is None:
                    self.pushError(self.methodStack[i+1], "var is not defined", ctx.start.line, 401)
                    sys.exit(1)
            if self.semantica.checkFunctionExists(self.semantica.getClase(myVar.tipo), str(ctx.mcall().ID())) == False:
                    self.pushError(str(ctx.mcall().ID()), "method is not defined", ctx.start.line, 407)
                    sys.exit(1)
            self.mClass = myVar.tipo


        else:
            self.push(self.methodStack, str(ctx.ID()))

    def enterPv(self, ctx):
        self.isPublic = False
    
    def exitPv(self, ctx):
        self.isPublic = True



    def enterConditionsecond(self, ctx):
        expType = self.tope(self.tipoStack)
        if expType != 'int':
            #TODO("mark error")
            print("err")
        else:
            result = self.tope(self.expStack)
            self.pushCuadruplo('gotof', result , None, -1)
            self.push(self.jmpStack, len(self.cuadruplos)-1)

    def exitConditionsecond(self, ctx):
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
            self.pop(self.tipoStack)

    
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

    def enterImprimir(self, ctx):
        self.push(self.expStack, 'P')

    #TODO(crear quad)
    def exitImprimir(self, ctx):
        myExps = []
        while len(self.expStack) > 0 and self.tope(self.expStack) != 'P':
            self.push(myExps, self.tope(self.expStack))
            self.pop(self.expStack)
            self.pop(self.tipoStack)

        if len(self.expStack) > 0 and self.tope(self.expStack) == 'P':
            self.pop(self.expStack)

        while len(myExps) > 0:
            self.pushCuadruplo('print', None, None, self.tope(myExps))
            self.pop(myExps)








    def tope(self, stack):
        return stack[len(stack)-1]

    def push(self, stack, val):
        stack.append(val)

    def pop(self, stack):
        stack.pop()

    def enterCte(self, ctx):
        tipos = 'void'
        if ctx.INT() is not None:
            val = ctx.INT()
            tipos = 'int'
        elif ctx.FLOAT() is not None:
            val = ctx.FLOAT()
            tipos = 'float'
        elif ctx.CHAR() is not None:
            val = ctx.CHAR()
            tipos = 'char'
        self.push(self.expStack, str(val))
        self.push(self.tipoStack, tipos)


    
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
                    sys.exit(1)

                if resultT != "err":
                    resultAddress = self.semantica.getAddress(resultT, True)
                    self.pushCuadruplo(operando, left, right, resultAddress)
                    self.push(self.expStack, resultAddress)
                    self.push(self.tipoStack, resultT)
                else:
                    self.err.push("type mismatch : "+leftT+" and "+rightT+" | line "+str(ctx.start.line), 403)
                    sys.exit(1)

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
                    sys.exit(1)

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
                    sys.exit(1)




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

    def enterExpaux(self, ctx):
        self.push(self.opStack, str(ctx.binbasico().getChild(0)))

    def exitExpaux(self, ctx):
        self.resolveExp(ctx)

    def exitExp(self, ctx):
        self.resolveExp(ctx)

    def enterTermaux(self, ctx):
        self.push(self.opStack, str(ctx.bincomplejo().getChild(0)))
        

    def pushError(self, fToken, msg, line, code):
        linea = str(line)
        self.err.push("\'"+str(fToken)+"\' " + msg + " | line : " + linea, code)


    def enterFparam(self, ctx):
        self.push(self.expStack, '#')
        self.push(self.parameters, 'T')
        self.push(self.tipos, 'T')


    

    def exitFparam(self, ctx):
        while len(self.expStack) > 0 and self.tope(self.expStack) != '#':
            param1 = self.tope(self.expStack)
            tipo1 = self.tope(self.tipoStack)
            self.pop(self.expStack)
            self.pop(self.tipoStack)
            self.push(self.parameters, param1)
            self.push(self.tipos, tipo1)

        if len(self.expStack) > 0 and self.tope(self.expStack) == '#':
            self.pop(self.expStack)


        
    def compareFunctions(self, funcA):
        myParameters = []
        myTypes = []


        while len(self.parameters) > 0 and self.tope(self.parameters) != 'T':
            param1 = self.tope(self.parameters)
            tipo1 = self.tope(self.tipos)
            
            self.push(myParameters, param1)
            self.push(myTypes, tipo1)
    
            self.pop(self.parameters)
            self.pop(self.tipos)

        if len(self.parameters) > 0 and self.tope(self.parameters) == 'T':
            self.pop(self.parameters)

        return self.semantica.canUseFunction(funcA, myParameters, myTypes)


    def exitFunccall(self, ctx):
        if self.semantica.checkFunctionExists(self.tope(self.classStack), str(ctx.ID())) == False:
            fToken = ctx.ID()
            self.err.push("\'"+str(fToken)+"\' function not declared | line : "+str(ctx.start.line), 402)
            sys.exit(1)
        else:
            myFunc = self.semantica.getFunc(self.tope(self.classStack),  str(ctx.ID()))
            if self.compareFunctions(myFunc) == False:
                self.pushError(str(ctx.ID()), "the function doesnt not match", ctx.start.line, 409)
                sys.exit(1)

            self.push(self.expStack, myFunc.getReturnDir())
            self.push(self.tipoStack, myFunc.tipoRetorno)






        

    def exitFactorclases(self, ctx):
        # func call
        if ctx.PA() is not None and ctx.PUNTO() is None:
            if self.semantica.checkFunctionExists(self.tope(self.classStack), str(ctx.ID(0))) == False:
                fToken = ctx.ID(0)
                self.pushError(fToken, "function not declared", ctx.start.line, 402)
                sys.exit(1)
            else:
                #ok, it does exist, but is it the same?
                myFunc = self.semantica.getFunc(self.tope(self.classStack), str(ctx.ID(0)))
                if self.compareFunctions(myFunc) == False:
                    self.pushError(str(ctx.ID(0)), "the function doesnt not match", ctx.start.line, 409)
                    sys.exit(1)

                if myFunc.tipoRetorno == 'void':
                    self.pushError(str(ctx.ID(0)), "the function has type return void", ctx.start.line, 408)
                    sys.exit(1)
                else:
                    self.push(self.expStack, myFunc.getReturnDir())
                    self.push(self.tipoStack, myFunc.tipoRetorno)


                #atributos && metodos de clases
        elif ctx.PUNTO() is not None:
            varName = str(ctx.ID(0))
            

            myVar = self.semantica.existVariable(self.tope(self.classStack), self.tope(self.funcStack).name, varName)

            if myVar is None:
                self.pushError(varName, "variable not declared", ctx.start.line, 401)
                sys.exit(1)

            className = myVar.tipo
            myFunc = self.semantica.getFunc(self.semantica.getClase(className), str(ctx.ID(1)))


    
            cls = self.semantica.getClase(className)
            if cls == None:
                #throw error
                self.pushError(className, "class not declared", ctx.start.line, 405)
                sys.exit(1)
                #metodos

            if ctx.PA() != None:
                metodoName = str(ctx.ID(1))
                if self.semantica.checkFunctionExists(cls, metodoName) == False:
                    self.pushError(metodoName, "method not declared", ctx.start.line, 407)
                    sys.exit(1)
                else:
                    #ok, it does exist, but is it the same?
                    if self.compareFunctions(myFunc) == False:
                        self.pushError(metodoName, "the function doesnt not match", ctx.start.line, 409)
                        sys.exit(1)

                    myFunc = self.semantica.getFunc(cls, metodoName)
                    if myFunc.tipoRetorno == 'void':
                        self.pushError(metodoName, "the method has type return void", ctx.start.line, 408)
                        sys.exit(1)
                    else:
                        self.push(self.expStack, myFunc.getReturnDir())
                        self.push(self.tipoStack, myFunc.tipoRetorno)
            else:
                #atributo
                attrName = str(ctx.ID(1))
               
                elem = self.semantica.existVariable(cls, self.tope(self.funcStack).name, attrName)
                if elem == None:
                    #throw error
                    self.pushError(attrName, "attribute not declared inside the class", ctx.start.line, 406)
                    sys.exit(1)

                self.push(self.expStack, elem.direccion)
                self.push(self.tipoStack, elem.tipo)
                

                

        # variable 
        else:
            elemento  = self.semantica.existVariable(self.tope(self.classStack), self.tope(self.funcStack).name, str(ctx.ID(0)))
            if elemento == None:
                fToken = ctx.ID(0)
                self.err.push("\'"+str(fToken)+"\' is not defined | line : " + str(ctx.start.line), 401)
            else:
                #TODO(FIX)
                #TODO(Cte doesnt have a tipo)
                self.push(self.expStack, str(ctx.ID(0)))
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


