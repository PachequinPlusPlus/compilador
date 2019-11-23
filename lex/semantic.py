from variable import variable
from clases import clase
from funcion import funcion
from memory import memoria

import json

# nombre | direcion
class semantics:
    scopes = ["global"]
    types = []
    funcs = []



                    # consider just integers
    classes = []

    memo = memoria(100000, 110000, 120000)





    def __init__(self):
        self.clases = []


    
    def getDireccion(self, base, pos):
        return self.classes[base+pos]



    def pr(self):
        parsed =str(self.clases).replace("'", '"')
        parsed = parsed.replace("False", 'false')
        parsed = parsed.replace("True", 'true')
        parsed = parsed.replace("None", '"None"')
        parsed2 = json.loads(parsed)
        #print(self.memo)



    def getAddressGlobal(self, tipo, globalClass):
        #TODO(que hacer para las clases?)
        if tipo == "int":
            return globalClass.memoriaGlobal.getEntera()
        elif tipo == "float":
            return globalClass.memoriaGlobal.getFlotante()
        elif tipo == "char":
            return globalClass.memoriaGlobal.getChar() 
        else:
            #it's a class! 
            cl = self.getClase(tipo)
            initial = len(self.classes)
            sz = cl.getVariables()
            while ( sz > 0):
                sz = sz - 1
                self.classes.append(0)

            idx = int(initial)
            for elem in cl.publicAtributos:
                if elem.tipo == 'int':
                    self.classes[idx] = (self.memo.getEntera())
                elif elem.tipo == 'char':
                    self.classes[idx] = (self.memo.getChar())
                elif elem.tipo == 'float':
                    self.classes[idx] = (self.memo.getFloat())
                else:
                    self.classes[idx] = getAddressGlobal(elem.tipo, globalClass)
                    # it's a class, wtf?
                idx = idx + 1

            for elem in cl.privateAtributos:
                if elem.tipo == 'int':
                    self.classes[idx] = (self.memo.getEntera())
                elif elem.tipo == 'char':
                    self.classes[idx] = (self.memo.getChar())
                elif elem.tipo == 'float':
                    self.classes[idx] = (self.memo.getFloat())
                else:
                    self.classes[idx] = self.getAddressGlobal(elem.tipo, globalClass)
                    # it's a class, wtf?
                idx = idx + 1



            return initial

                
    
    #TODO(correguir las address temporales)
    #TODO(agregar memoria para los metodos con return?)
    def getAddressFunc(self, tipo, func):
        #TODO(que hacer para las clases?)
        if tipo == "int":
            return func.memory.getEntera()
        elif tipo == "float":
            return func.memory.getFlotante()
        elif tipo == "char":
            return func.memory.getChar() 
        else:
            #it's a class! 
            cl = self.getClase(tipo)
            initial = len(self.classes)
            sz = cl.getVariables()
            while ( sz > 0):
                sz = sz - 1
                self.classes.append(0)

            idx = int(initial)
            for elem in cl.publicAtributos:
                if elem.tipo == 'int':
                    self.classes[idx] = (self.memo.getEntera())
                elif elem.tipo == 'char':
                    self.classes[idx] = (self.memo.getChar())
                elif elem.tipo == 'float':
                    self.classes[idx] = (self.memo.getFloat())
                else:
                    self.classes[idx] = self.getAddressFunc(elem.tipo, func)
                    # it's a class, wtf?
                idx = idx + 1

            for elem in cl.privateAtributos:
                if elem.tipo == 'int':
                    self.classes[idx] = (self.memo.getEntera())
                elif elem.tipo == 'char':
                    self.classes[idx] = (self.memo.getChar())
                elif elem.tipo == 'float':
                    self.classes[idx] = (self.memo.getFloat())
                else:
                    self.classes[idx] = self.getAddressFunc(elem.tipo, func)
                    # it's a class, wtf?
                idx = idx + 1



            return initial

             


    def reverseStack(self, stack):
        reversed = []
        while len(stack) > 0:
            self.push(reversed, self.tope(stack))
            self.pop(stack)
        return reversed


    #ideally, this should be call after checking with checkFunction Exists
    def getFunc(self, clase, funcName, isPublic = True):
        for cl in self.clases:
            if cl.name == clase.name:
                for func in cl.publicMetodos:
                    if func.name == funcName:
                        return func
                for func in cl.privateMetodos:  
                    if isPublic and func.name == funcName:
                        return func
                if cl.parent is not None:
                    return self.getFunc(self.getClase(cl.parent), funcName, False)

        #because of 73, this should never return None
        return None


    #check if you can call funcA with params and types
    def canUseFunction(self, funcA, params, tipos):
        if len(funcA.params) != len(params):
            return False

        
        for i in range(len(params)):
            if funcA.params[len(params) - i - 1].tipo != tipos[i]:
                return False

        return True



    #TODO(checar que tenga el mismo numero de parametros)
    def checkFunctionExists(self, clase, funcName, isPublic = True):
        for cl in self.clases:
            if cl.name == clase.name:
                for func in cl.publicMetodos:
                    if func.name == funcName:
                        return True
                for func in cl.privateMetodos:  
                    if isPublic and func.name == funcName:
                        return True
                if cl.parent is not None:
                    return self.checkFunctionExists(self.getClase(cl.parent), funcName, False)
        return False

    def getClase(self, className):
        for cl in self.clases:
            if cl.name == className:
                return cl
        return None

    def existInClass(self, clase, varName):
        for cl in self.clases:
            if cl.name == clase.name:
                for atr in cl.publicAtributos:
                    if atr.name == varName:
                        return atr
                for atr in cl.privateAtributos:
                    if atr.name == varName:
                        return atr

                actual = cl

                while actual.parent is not None:
                    actual = self.getClase(actual.parent)
                    for atr in actual.publicAtributos:
                        if atr.name == varName:
                            return atr
        return None



    #TODO(optimizar esto)
    # estamos mandando el nombre de la clase, en vez de mandar la instancia directamente duuhh
    def existVariable(self, clase, funcName, varName):
        for cl in self.clases:
            if cl.name == clase.name:
                for func in cl.publicMetodos:
                    if func.name == funcName:
                        for param in func.params:
                            if param.name == varName:
                                return param
                        for var in func.vars:
                            if var.name == varName:
                                return var
                        
                for func in cl.privateMetodos:  
                    if func.name == funcName:
                        if func.name == funcName:
                            for param in func.params:
                                if param.name == varName:
                                    return param
                            for var in func.vars:
                                if var.name == varName:
                                    return var
                for atr in cl.publicAtributos:
                    if atr.name == varName:
                        return atr
                for atr in cl.privateAtributos:
                    if atr.name == varName:
                        return atr



                actual = cl

                while actual.parent is not None:
                    actual = self.getClase(actual.parent)
                    for atr in actual.publicAtributos:
                        if atr.name == varName:
                            return atr
        return None
       
    def tope(self, lista):
        if len(lista) == 0:
            return -1
        fr = lista[len(lista)-1]
        return fr

    # new functions
    #-------------------------------------------------------------------------------
    def appendClass(self, clase):
        self.clases.append(clase)

    def addClass(self, className, parent):
        self.clases.append(clase(className, parent))
        return self.tope(self.clases)

    # add a function into a class
    def addFunction(self, clase, isPublic, funcName, tipoRetorno, ip):
        for cls in self.clases:
            if clase == cls:
                clase.appendFunction(funcion(funcName, tipoRetorno, ip), isPublic)
                return clase.getFunction(isPublic)


    # add an attribute into a class
    def addAtributo(self, clase, varName, tipo, direccion, isArray, isPublic, arrSize):
        clase.appendAtributo(variable(varName, tipo, direccion, isArray, arrSize, clase.getVariables()), isPublic)

    # add param into a function
    #is array is always suppose to be false!!
    def addParameter(self, func, name, tipo, direccion, isArray):
        func.appendParam(variable(name, tipo, direccion, isArray, -1, func.numberParams))


    # add var into a function
    def addVarFunc(self, func, name, tipo, direccion, isArray, arrSize = -1):
        func.appendVar(variable(name, tipo, direccion, isArray, arrSize, len(func.vars)))

    #-------------------------------------------------------------------------------
        








    cube = {
            'int' : {
                    'int' : {
                            '+' : 'int',
                            '-' : 'int',
                            '/' : 'int',
                            '*' : 'int',
                            '<' : 'int',
                            '<=' : 'int',
                            '>' : 'int',
                            '>=' : 'int',
                            '==' : 'int',
                            '!=' : 'int',
                            '&&' : 'int',
                            '||' : 'int'
                        },
                    'float' : {
                            '+' : 'float',
                            '-' : 'float',
                            '/' : 'float',
                            '*' : 'float',
                            '<' : 'int',
                            '<=' : 'int',
                            '>' : 'int',
                            '>=' : 'int',
                            '==' : 'int',
                            '!=' : 'int',
                            '&&' : 'err',
                            '||' : 'err'
                        },
                    'char' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err',
                            '<' : 'err',
                            '<=' : 'err',
                            '>' : 'err',
                            '>=' : 'err',
                            '==' : 'err',
                            '!=' : 'err',
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
                            '<=' : 'int',
                            '>' : 'int',
                            '>=' : 'int',
                            '==' : 'int',
                            '!=' : 'int',
                            '&&' : 'err',
                            '||' : 'err'
                        },
                    'float' : {
                            '+' : 'float',
                            '-' : 'float',
                            '/' : 'float',
                            '*' : 'float',
                            '<' : 'int',
                            '<=' : 'int',
                            '>' : 'int',
                            '>=' : 'int',
                            '==' : 'int',
                            '!=' : 'int',
                            '&&' : 'err',
                            '||' : 'err'
                        },
                    'char' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err',
                            '<' : 'err',
                            '<=' : 'err',
                            '>' : 'err',
                            '>=' : 'err',
                            '==' : 'err',
                            '!=' : 'err',
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
                            '<=' : 'err',
                            '>' : 'err',
                            '>=' : 'err',
                            '==' : 'err',
                            '!=' : 'err',
                            '&&' : 'err',
                            '||' : 'err'
                        },
                    'float' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err',
                            '<' : 'err',
                            '<=' : 'err',
                            '>' : 'err',
                            '>=' : 'err',
                            '==' : 'err',
                            '!=' : 'err',
                            '&&' : 'err',
                            '||' : 'err'
                        },
                    'char' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err',
                            '<' : 'int',
                            '<=' : 'int',
                            '>' : 'int',
                            '>=' : 'int',
                            '==' : 'int',
                            '!=' : 'int',
                            '&&' : 'err',
                            '||' : 'err'
                        }
                }
    }

