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
from memory import memoria

import sys



class PPCDSALVCCustomListener(PPCDSALVCListener):
                            #enteras #flotantes #chars
    #la memoria de constantes?
    constantes = memoria(61000, 71000, 81000)
    #vamo a usar un dic para mapear las dir ya declaradas
    myCte = {}

    #a conseguir el valor back
    myCteB = {}


    # CTES
    offSetClass = 5000

    #Boleanos
    isClass = False
    isFunction = False
    isParameter = False
    isPublic = True

    # ints
    numberParams = 0
    arrSize = 0

    offSetI = 0
    offSetf = 0
    offSetc = 0

    offSet = 0


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
    jmpLoop = []
    assStack = []

    parameters = []
    tipos = []
    methodStack = []


    # stack para clases y funciones
    classStack = []
    funcStack = []


    def enterAssignment(self, ctx):
        #meter todos los ids
        self.push(self.assStack, str(ctx.ID()))



    def exitAssignment(self, ctx):
        if ctx.IGUAL() is not None:
            # clase en donde empieza a buscar
            cls = self.tope(self.classStack)

            # en que funcion estas
            func = self.tope(self.funcStack).name


            # x.y.z = exp
            # this is X
            # x = exp
            left = self.semantica.existVariable(cls, func, self.assStack[0])
            direccion  = left.direccion # direccion Base 
            # cls will contain the final class to get the variable
            cls = self.semantica.getClase(left.tipo)
    
            if left.tipo == 'int' or left.tipo == 'char' or left.tipo =='float':
                cls = self.tope(self.classStack)


            for i in range(len(self.assStack)-2):
                left = self.semantica.existVariable(cls, func, self.assStack[i+1], False)
                if left == None:
                    self.pushError(self.assStack[i+1], "is not declared", ctx.start.line, 499)
                    sys.exit(1)
                elif left.tipo == 'int' or left.tipo == 'char' or left.tipo == 'float':
                    self.pushError(self.assStack[i+1], "is not a class", ctx.start.line, 501)
                    sys.exit(1)

                direccion = direccion + left.direccion
                cls = self.semantica.getClase(left.tipo)


            left = self.semantica.existVariable(cls, func, self.tope(self.assStack), False)
            if left is None:
                self.pushError(self.tope(self.assStack), "is not declared", ctx.start.line, 499)
                sys.exit(1)
            elif left.tipo != 'int' and left.tipo != 'char' and left.tipo != 'float':
                print(left)
                self.pushError(self.tope(self.assStack), "is not an attribute", ctx.start.line, 502)

            if(len(self.assStack) > 1):
            # get the direction
                direccion =  direccion + left.direccion 

            if ctx.LB() is not None:
                rightValue = self.tope(self.expStack)
                self.pop(self.expStack)
                self.pop(self.tipoStack)

                sz = self.tope(self.expStack)
                self.pop(self.expStack)
                self.pop(self.tipoStack)

                if left.isArray is False:
                    self.pushError(elemento, "is not an array", ctx.start.line, 513)
                    sys.exit(1)

                resultAddress = -1
                if sz >= 61000 and sz <= 71000:
                    sz = int(self.myCteB[sz])
                    resultAddress = sz
                else:
                    resultAddress = self.getAddress('int')
                    self.pushCuadruplo('+_val_address', sz, direccion,  resultAddress)
                    sz = resultAddress

                size = left.array.getSize()
                self.pushCuadruplo('VALID', 0 , size, sz)

                self.push(self.expStack, rightValue)
                direccion = resultAddress



            self.pushCuadruplo('=', None , self.tope(self.expStack), direccion)

            # saco el EXP del stack
            self.pop(self.expStack)

            self.assStack = []




    # simbolos especiales
    condicionales = ['<', '<=', '>', '>=', '==', '!=']
    logical = ['&&', '||']

    def enterPrograma(self, ctx):
        self.push(self.classStack, self.semantica.addClass("global", None))
        self.pushCuadruplo('goto', None , None, -1)

    def exitPrograma(self, ctx):
        pass

    def enterCiclo(self, ctx):
        self.push(self.jmpLoop, len(self.cuadruplos))


    def exitWhilecond(self, ctx):
        expType = self.tope(self.tipoStack)
        if expType != 'int':
            self.pushError(expType, "is returned instead of an int", ctx.start.line, 411)
            sys.exit(1)
        else:
            result = self.tope(self.expStack)
            self.pop(self.expStack)
            self.pop(self.tipoStack)
            self.pushCuadruplo('gotof', result , None, -1)
            self.push(self.jmpLoop, len(self.cuadruplos)-1)

    def exitCiclo(self, ctx):
        jmp = self.tope(self.jmpLoop)
        self.pop(self.jmpLoop)
        
        jmp2 = self.tope(self.jmpLoop)
        self.pop(self.jmpLoop)

        self.pushCuadruplo('goto', None , None, jmp2)
        self.cuadruplos[jmp].result = len(self.cuadruplos)


        

    #quiero sacar de la pila a donde empieza la cond
    def exitfciclo(self, ctx):
        self.pop(self.jmpLoop)


    def enterFciclocond(self, ctx):
        self.push(self.jmpLoop, len(self.cuadruplos))

    def exitFciclocond(self, ctx):
        expType = self.tope(self.tipoStack)
        if expType != 'int':
            self.pushError(expType, "is returned instead of an int", ctx.start.line, 411)
            sys.exit(1)
        else:
            result = self.tope(self.expStack)
            self.pop(self.expStack)
            self.pop(self.tipoStack)
            self.pushCuadruplo('gotof', result , None, -1)
            self.push(self.jmpLoop, len(self.cuadruplos)-1)

            #goto to the body
            self.pushCuadruplo('goto', None, None, -1)
            self.push(self.jmpLoop, len(self.cuadruplos)-1)

    def enterFcicloupd(self, ctx):
        #a donde debe ir el body
        self.push(self.jmpLoop, len(self.cuadruplos))
    
    def exitFcicloupd(self, ctx):
        jmp = self.jmpLoop[len(self.jmpLoop) - 4]
        self.pushCuadruplo('goto', None, None, jmp)
        

    def enterFciclobody(self, ctx):
        jmp = self.jmpLoop[len(self.jmpLoop) - 2]
        self.cuadruplos[jmp].result = len(self.cuadruplos)
        
    def exitFciclobody(self, ctx):
        jmp = self.jmpLoop[len(self.jmpLoop) - 1]

        self.pop(self.jmpLoop);
        self.pop(self.jmpLoop);
        self.pushCuadruplo('goto', None, None, jmp)

        jmp = self.jmpLoop[len(self.jmpLoop) - 1]
        self.cuadruplos[jmp].result = len(self.cuadruplos)

        

        
    def getReturnAddrs(self, funcName, clase):
        funcName = 'r_'+funcName
        return self.semantica.existVariable(clase, self.tope(self.funcStack).name, funcName).direccion 




    def getActualIP(self):
        return len(self.cuadruplos)

    def exitFunctionbloque(self, ctx):
        if ctx.rt() is not None:
            if self.returnType == 'void':
                self.pushError('return', "was found but the function is void", ctx.start.line, 477)
                sys.exit(1)
            tipo = self.tope(self.tipoStack)
            if tipo != self.returnType:
                self.pushError(tipo, f"was found but the function is expecting to return {self.returnType}", ctx.start.line, 488)
                sys.exit(1)

            addr = self.getReturnAddrs(self.tope(self.funcStack).name, self.tope(self.classStack))
            right = self.tope(self.expStack)
            self.pop(self.expStack)
            self.pop(self.tipoStack)

            self.pushCuadruplo('=', None, right, addr)
        

                


    def getCteDir(self, val, tipo):
        if self.myCte.get(val) is not None:
            return self.myCte[val]
        if tipo == 'int':
            op = 'CI'
            self.myCte[val] = self.constantes.getEntera()
        elif tipo == 'float':
            op = 'CF'
            self.myCte[val] = self.constantes.getFlotante()
        elif tipo == 'char':
            op = 'CC'
            self.myCte[val] = self.constantes.getChar()

        self.pushCuadruplo(op, None , val, self.myCte[val])
        self.myCteB[self.myCte[val]] = val
        return self.myCte[val]








    # check that the method being call is valid
    def exitMcall(self, ctx):
        if self.semantica.checkFunctionExists(self.semantica.getClase(self.mClass), str(ctx.ID())) == False:
            fToken = ctx.ID()
            self.err.push("\'"+str(fToken)+"\' function not declared | line : "+str(ctx.start.line), 402)
            sys.exit(1)
        else:
            myFunc = self.semantica.getFunc(self.semantica.getClase(self.mClass),  str(ctx.ID()))
            # ERA
            self.pushCuadruplo('ERA', None , myFunc.size, myFunc.name)
            self.pushCuadruplo('SET', None , None, self.offSet)
            if self.compareFunctions(myFunc) == False:
                self.pushError(str(ctx.ID()), "the function doesnt not match", ctx.start.line, 409)
                sys.exit(1)

            #TODO(execute all here)
            if myFunc.tipoRetorno == 'void':
                return


            self.push(self.expStack, self.getReturnAddrs(myFunc.name, self.semantica.getClase(self.mClass))) # myFunc.getReturnDir())
            self.push(self.tipoStack, myFunc.tipoRetorno)



    # check that all the subclases exists for the method
    def enterMethod(self, ctx):
        if ctx.mcall() is not None:
            self.push(self.methodStack, str(ctx.ID()))
            #do something
            self.offSet = 0

            myVar = self.semantica.existVariable(self.tope(self.classStack), self.tope(self.funcStack).name, self.methodStack[0])
            self.offSet = self.offSet + myVar.direccion

            if myVar is None:
                self.pushError(self.methodStack[0], "var is not defined", ctx.start.line, 401)
                sys.exit(1)
            for i in range(len(self.methodStack)-1):
                myVar = self.semantica.existInClass(self.semantica.getClase(myVar.tipo), self.methodStack[i+1])
                if myVar is None:
                    self.pushError(self.methodStack[i+1], "var is not defined", ctx.start.line, 401)
                    sys.exit(1)
                self.offSet = self.offSet + myVar.direccion

            #checa que el ultimo sea un metodo definido
            if self.semantica.checkFunctionExists(self.semantica.getClase(myVar.tipo), str(ctx.mcall().ID()), False) == False:
                    self.pushError(str(ctx.mcall().ID()), "method is not defined", ctx.start.line, 407)
                    sys.exit(1)
            self.mClass = myVar.tipo

            self.methodStack = []

        else:
            self.push(self.methodStack, str(ctx.ID()))

    def enterPv(self, ctx):
        self.isPublic = False
    
    def exitPv(self, ctx):
        self.isPublic = True

    def enterCondition(self, ctx):
        self.push(self.jmpStack, 'F')


    def enterConditionsecond(self, ctx):
        expType = self.tope(self.tipoStack)
        if expType != 'int':
            self.pushError(expType, "is returned instead of an int", ctx.start.line, 411)
            sys.exit(1)
        else:
            result = self.tope(self.expStack)
            self.pop(self.expStack)
            self.pop(self.tipoStack)

            self.pushCuadruplo('gotof', result , None, -1)
            self.push(self.jmpStack, len(self.cuadruplos)-1)

    # entrando al elseif es cuando ya sabes cual es la exp, es cuando termina de hacer los statements, ya sabemos a donde va el primer if
    def enterElseif(self, ctx):
        #goto from the last condition
        #terminaste el primer if, ya salta al final
        self.pushCuadruplo('goto', None, None, -1)


        #goto from the first if( if it's false, move here)
        #lo que siga despues del goto ya no esta dentro de lif, so yeah
        jmp = self.tope(self.jmpStack)
        self.pop(self.jmpStack)
        self.cuadruplos[jmp].result = len(self.cuadruplos)


        #mete el goto que tenias pendiente a la pila de saltos
        #aun necesitamos saber a donde va
        self.push(self.jmpStack, len(self.cuadruplos)-1)


    # ok tenemos un elseif
    def enterConditionthird(self, ctx):
        expType = self.tope(self.tipoStack)
        if expType != 'int':
            self.pushError(expType, "is returned instead of an int", ctx.start.line, 411)
            sys.exit(1)
        else:
            # el gotof del elseif
            result = self.tope(self.expStack)
            #sacamos la exp y el tipo
            self.pop(self.expStack)
            self.pop(self.tipoStack)

            self.pushCuadruplo('gotof', result , None, -1)
            self.push(self.jmpStack, len(self.cuadruplos)-1)


    def enterElseotr(self, ctx):
        #goto from the else if
        #ya terminaste el elseif, salte hasta el final de la condicional
        self.pushCuadruplo('goto', None, None, -1)


        
        # jmp en falso
        jmp = self.tope(self.jmpStack)
        self.pop(self.jmpStack)
        self.cuadruplos[jmp].result = len(self.cuadruplos)

        
        self.push(self.jmpStack, len(self.cuadruplos)-1)


    def exitCondition(self, ctx):
        while( self.tope(self.jmpStack) != 'F'):
            #goto del if/ goto del elseif
            jmp = self.tope(self.jmpStack)
            self.pop(self.jmpStack)
            self.cuadruplos[jmp].result = len(self.cuadruplos)
        self.pop(self.jmpStack)



    def insertVariablesPadres(self, ctx):
        cl = self.tope(self.classStack)
        parent = cl.parent
        if(parent == 'global'):
            return
        cl = self.semantica.getClase(parent)
        while( cl.name != 'global'):
            for variable in cl.publicAtributos:
                sz = -1
                if variable.array is not None:
                    sz  = variable.array.getSize()
                self.insertVar(variable.name, ctx, variable.isArray, sz)
                if cl.parent == None:
                    return
            cl = self.semantica.getClase(cl.parent)


    def enterClasses(self, ctx):
        self.isClass = True
        name = str(ctx.ID(0))
        if ctx.PP() is not None:
            parent = str(ctx.ID(1))
            cl = self.tope(self.classStack)
            self.push(self.classStack, self.semantica.addClass(name, parent))
            self.insertVariablesPadres(ctx)
        else:
            cl = self.tope(self.classStack)
            self.push(self.classStack, self.semantica.addClass(name, "global",))

    def exitClasses(self, ctx):
        self.isClass = False
        self.pop(self.classStack)
            



    def enterParameters(self, ctx):
        self.isParameter = True

    def exitParameters(self, ctx):
        self.isParameter = False

    
    
    def insertVar(self, varName, ctx, isArray = False, arrSize = -1):
       tipo = self.lastType
       if tipo != 'int' and tipo != 'char' and tipo != 'float':
           #check the class exists
           if self.semantica.getClase(tipo) is None:
               self.pushError(tipo, "class doesnt exists", ctx.start.line, 506)
               sys.exit(1)


        
       if self.isFunction:
           if self.semantica.existVariable(self.tope(self.classStack), self.tope(self.funcStack).name, varName) is not None:
               self.pushError(varName, "is already declared", ctx.start.line, 455)
               sys.exit(1)

           if self.isParameter:
               self.semantica.addParameter(self.tope(self.funcStack), varName, tipo, self.getAddress(tipo), False)
           else:
               self.semantica.addVarFunc(self.tope(self.funcStack), varName, tipo, self.getAddress(tipo, isArray, arrSize), isArray, arrSize)
       else:
           topeClase = self.tope(self.classStack)
           if self.semantica.existInClass(topeClase, varName, False) is not None:
               self.pushError(varName, "is already declared", ctx.start.line, 455)
               sys.exit(1)
           #TODO(arreglar isArray)
           self.semantica.addAtributo(self.tope(self.classStack), varName, tipo, self.getAddress(tipo, isArray, arrSize), isArray, self.isPublic, arrSize)
       return

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

        cteDir = self.getCteDir(str(val), tipos)
        self.push(self.expStack, cteDir)
        self.push(self.tipoStack, tipos)


    
    def enterFactor(self, ctx):
        pass       

    

    def getAddress(self, tipo, isArray = False, arraySize = 0):
        if len(self.funcStack) == 0:
            #should be global
            add = self.semantica.getAddressGlobal(tipo, self.tope(self.classStack))
            for i in range(arraySize):
                self.semantica.getAddressGlobal(tipo, self.tope(self.classStack))
            return add
        else:
            add = self.semantica.getAddressFunc(str(tipo), self.tope(self.funcStack))
            for i in range(arraySize):
                self.semantica.getAddressFunc(str(tipo), self.tope(self.funcStack))
            return add

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
                    resultAddress = self.getAddress(resultT)
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
                # error because ? mhm not sure why, guess cause of bad operands?
                #are we considering leftT and righT to actually be address?
                try:
                    resultT = self.semantica.cube[leftT][rightT][operando]
                except:
                    self.err.push("tmp, err", 404)
                    sys.exit(1)

                if resultT != "err":
                    resultAddress = self.getAddress(resultT)
                    self.pushCuadruplo(operando, left, right, resultAddress)
                    self.push(self.expStack, resultAddress)
                    self.push(self.tipoStack, resultT)
                else:
                    self.err.push("type mismatch : "+leftT+" and "+rightT+" | line "+str(ctx.start.line), 403)
                    sys.exit(1)


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
                    resultAddress = self.getAddress(resultT)
                    self.pushCuadruplo(operando, left, right, resultAddress)
                    self.push(self.expStack, resultAddress)
                    self.push(self.tipoStack, resultT)
                else:
                    self.err.push("type mismatch : "+leftT+" and "+rightT+" | line "+str(ctx.start.line), 403)
                    sys.exit(1)


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
                    resultAddress = self.getAddress(resultT)
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
        self.push(self.opStack, '#')
        self.push(self.parameters, 'T')
        self.push(self.tipos, 'T')


    

    def exitFparam(self, ctx):
        while len(self.expStack) > 0 and self.tope(self.expStack) != '#' and len(self.tipoStack) > 0:
            param1 = self.tope(self.expStack)
            tipo1 = self.tope(self.tipoStack)
            self.pop(self.expStack)
            self.pop(self.tipoStack)
            self.push(self.parameters, param1)
            self.push(self.tipos, tipo1)

        if len(self.expStack) > 0 and self.tope(self.expStack) == '#':
            self.pop(self.expStack)

        if len(self.opStack) > 0 and self.tope(self.opStack) == '#':
            self.pop(self.opStack)


        
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

        
        if self.semantica.canUseFunction(funcA, myParameters, myTypes):
            for i in range(len(myParameters)):
                self.pushCuadruplo('param', myParameters[i], None, funcA.params[i].direccion)

            self.pushCuadruplo('gosub', funcA.name, None, funcA.ip)
            return True

        return False


    def exitFunccall(self, ctx):
        if self.semantica.checkFunctionExists(self.tope(self.classStack), str(ctx.ID())) == False:
            fToken = ctx.ID()
            self.err.push("\'"+str(fToken)+"\' function not declared | line : "+str(ctx.start.line), 402)
            sys.exit(1)
        else:
            #create function
            myFunc = self.semantica.getFunc(self.tope(self.classStack),  str(ctx.ID()))
            self.pushCuadruplo('ERA', None , myFunc.size, myFunc.name)

            dirr = self.tope(self.classStack).offSet
            # set offset back to zero
            self.pushCuadruplo('SET', None , None, dirr)

            if self.compareFunctions(myFunc) == False:
                self.pushError(str(ctx.ID()), "the function doesnt not match", ctx.start.line, 409)
                sys.exit(1)





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
                self.pushCuadruplo('ERA', None , myFunc.size, myFunc.name)
                if self.compareFunctions(myFunc) == False:
                    self.pushError(str(ctx.ID(0)), "the function doesnt not match", ctx.start.line, 409)
                    sys.exit(1)

                #set offset to the going function
                self.pushCuadruplo('SET', None , None, self.tope(self.classStack).offSet)

                if myFunc.tipoRetorno == 'void':
                    self.pushError(str(ctx.ID(0)), "the function has type return void", ctx.start.line, 408)
                    sys.exit(1)
                else:
                    #put the result from r_funcName into a temp
                    resultAddress = self.getAddress(myFunc.tipoRetorno)
                    rtn = self.getReturnAddrs(myFunc.name, self.tope(self.classStack))
                    self.pushCuadruplo('=',None , rtn, resultAddress)
                    self.push(self.expStack , resultAddress)
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
                if self.semantica.checkFunctionExists(cls, metodoName, False) == False:
                    self.pushError(metodoName, "method not declared", ctx.start.line, 407)
                    sys.exit(1)
                else:
                    #ok, it does exist, but is it the same?
                    myFunc = self.semantica.getFunc(cls, metodoName)

                    self.pushCuadruplo('ERA', None , myFunc.size, myFunc.name)
                    self.pushCuadruplo('SET', None , None, cls.offSet)
                    if self.compareFunctions(myFunc) == False:
                        self.pushError(metodoName, "the function doesnt not match", ctx.start.line, 409)
                        sys.exit(1)

                    if myFunc.tipoRetorno == 'void':
                        self.pushError(metodoName, "the method has type return void", ctx.start.line, 408)
                        sys.exit(1)
                    else:
                        self.push(self.expStack, self.getReturnAddrs(myFunc.name, cls))
                        self.push(self.tipoStack, myFunc.tipoRetorno)
            else:
                #atributo
                attrName = str(ctx.ID(1))
               
                elem = self.semantica.existVariable(cls, self.tope(self.funcStack).name, attrName, False)
                if elem == None:
                    #throw error
                    self.pushError(attrName, "attribute not declared inside the class", ctx.start.line, 406)
                    sys.exit(1)
                                        # clase + atributos direcciones
                self.push(self.expStack, myVar.direccion + elem.direccion )
                self.push(self.tipoStack, elem.tipo)
                

                

        # variable 
        else:
            elemento  = self.semantica.existVariable(self.tope(self.classStack), self.tope(self.funcStack).name, str(ctx.ID(0)))
            if elemento == None:
                fToken = ctx.ID(0)
                self.err.push("\'"+str(fToken)+"\' is not defined | line : " + str(ctx.start.line), 401)
                sys.exit(1)
            else:
                direccion = elemento.direccion
                if ( ctx.arreglo() is not None ):
                    # getting array size ? arr[exp]

                    if elemento.isArray is False:
                        self.pushError(elemento, "is not an array", ctx.start.line, 513)
                        sys.exit(1)


                    size = elemento.array.getSize()
                        # lo que apunet a esa direccion bro
                    self.pushCuadruplo('VALID', 0 , size, self.tope(self.expStack))
                    # sz to check

                    pos = -1

                    # dentro del rango de ctes enteras
                    if self.tope(self.expStack) >= 61000 and self.tope(self.expStack) <= 71000:
                        #  pos es el valor original de la cte
                        pos = direccion + int(self.myCteB[self.tope(self.expStack)])
                        self.pop(self.expStack)
                    else:
                        # i need to sum to elemento.direccion + X equivalent
                        # i need a temporal address
                        resultAddress = self.getAddress('int')
                                                            # what is in this address  sumaselo a esto  to this one y ponlo aqui
                        self.pushCuadruplo('+_val_address', self.tope(self.expStack), elemento.direccion,  resultAddress)
                        self.pop(self.expStack)
                        pos = resultAddress

                    self.push(self.expStack, pos) # str(ctx.ID(0)))
                    self.push(self.tipoStack, elemento.tipo)

                else:
                    self.push(self.expStack, elemento.direccion) # str(ctx.ID(0)))
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
            sonArreglos.append(ctx.typesvaraux().scte().INT())
        else:
            sonArreglos.append(-1)
                
        for act in ctx.secondType():
            indices.append(str(act.ID()))
            if act.LB() is not None:
                sonArreglos.append(act.scte().INT())
            else:
                sonArreglos.append(-1)


        i = 0
        while  i < len(indices):
            vr = indices[i]
            tope = int(str((sonArreglos[i])))
            self.insertVar(vr, ctx, tope != -1, tope)
            i = i + 1 
            



    def enterMain(self, ctx):
        self.cuadruplos[0].result = len(self.cuadruplos)
        self.isFunction=True
#        self.push(self.funcStack, funcion('main', 'void'))
        self.push(self.funcStack, self.semantica.addFunction(self.tope(self.classStack), True, 'main', 'void', self.getActualIP()))

        #        self.semantica.appendFuncs("main")

    def exitMain(self, ctx):
        self.isFunction = False
        self.pop(self.funcStack)

    def enterFunctions(self, ctx):
        nameFunction = str(ctx.ID())
        self.returnType = str(ctx.returntypes().getChild(0))
        if self.returnType != 'void':
            #i need a global variable named the same
            self.lastType = self.returnType
            self.insertVar('r_'+nameFunction, ctx, False, 0)
        self.isFunction = True
        self.push(self.funcStack, self.semantica.addFunction(self.tope(self.classStack), self.isPublic, nameFunction, self.returnType, self.getActualIP()))

    def exitFunctions(self, ctx):
        self.pushCuadruplo('endproc', None , None, None)
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



    def __init__(self, semantica, errores):
        self.semantica = semantica
        self.err = errores
        self.cuadruplos = []
            



    def exitTypesvar(self, ctx):
        pass


