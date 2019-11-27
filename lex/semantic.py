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



    classes = []






    def __init__(self):
        self.clases = []


    



    def pr(self):
        parsed =str(self.clases).replace("'", '"')
        parsed = parsed.replace("False", 'false')
        parsed = parsed.replace("True", 'true')
        parsed = parsed.replace("None", '"None"')
        parsed2 = json.loads(parsed)
        #print(json.dumps(parsed2, indent=4, sort_keys=True))


    # return the next global addres
    def getAddressGlobal(self, tipo, globalClass):
        #TODO(que hacer para las clases?)
        if tipo == "int":
            return globalClass.memoriaGlobal.getEntera()
        elif tipo == "float":
            return globalClass.memoriaGlobal.getFlotante()
        elif tipo == "char":
            return globalClass.memoriaGlobal.getChar() 
        else:
            # class set it to -1 for now
            return -1
                
    
    # this function returns the next local address for the function
    def getAddressFunc(self, tipo, func):
        if tipo == "int":
            return func.memory.getEntera()
        elif tipo == "float":
            return func.memory.getFlotante()
        elif tipo == "char":
            return func.memory.getChar() 
        else:
            # class, set it to -1 for now
            return -1

             


    # reverse the stack
    # just an utility function
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


    # check if a function exist within a className
    def checkFunctionExists(self, clase, funcName, canPrivate = True):
        for cl in self.clases:
            if cl.name == clase.name:
                for func in cl.publicMetodos:
                    if func.name == funcName:
                        return True
                for func in cl.privateMetodos:  
                    if canPrivate and func.name == funcName:
                        return True
                if cl.parent is not None:
                    return self.checkFunctionExists(self.getClase(cl.parent), funcName, False)
        return False

    # return a class with the className
    def getClase(self, className):
        for cl in self.clases:
            if cl.name == className:
                return cl
        return None

    # check if varName exist inside the class and its scope
    def existInClass(self, clase, varName, checkParent = True):
        for cl in self.clases:
            if cl.name == clase.name:
                for atr in cl.publicAtributos:
                    if atr.name == varName:
                        return atr
                for atr in cl.privateAtributos:
                    if atr.name == varName:
                        return atr

                actual = cl
                if checkParent is False:
                    return
                while actual.parent is not None:
                    actual = self.getClase(actual.parent)
                    for atr in actual.publicAtributos:
                        if atr.name == varName:
                            return atr
        return None



    # check if the variable exist within this scope
    def existVariable(self, clase, funcName, varName, canPrivate = True):
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
                    if canPrivate and func.name == funcName:
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
                    if canPrivate and atr.name == varName:
                        return atr



                actual = cl

                while actual.parent is not None:
                    actual = self.getClase(actual.parent)
                    for atr in actual.publicAtributos:
                        if atr.name == varName:
                            return atr
        return None
       
    # utility function to get top of stack
    def tope(self, lista):
        if len(lista) == 0:
            return -1
        fr = lista[len(lista)-1]
        return fr

    # new functions
    #-------------------------------------------------------------------------------

    # append a class into our class stack
    # it receives the class itself
    def appendClass(self, clase):
        self.clases.append(clase)

    # add a class to the current class abstract logic
    # it receives the className and the parent to the class
    # if the class doesnt has a parent, it will be global
    def addClass(self, className, parent):
        self.clases.append(clase(className, parent))
        return self.tope(self.clases)

    # add a function into a class
    #it receives the class where it will be hold, if it's public, the funcName, the return type and the instruction pointer
    def addFunction(self, clase, isPublic, funcName, tipoRetorno, ip):
        for cls in self.clases:
            if clase == cls:
                clase.appendFunction(funcion(funcName, tipoRetorno, ip), isPublic)
                return clase.getFunction(isPublic)


    # add an attribute into a class
    # it receives the class itself, the varname, the type, address, if it's ana array, if it public or private
    # and its arraySize if any
    def addAtributo(self, clase, varName, tipo, direccion, isArray, isPublic, arrSize):
        clase.appendAtributo(variable(varName, tipo, direccion, isArray, arrSize,), isPublic, self)

    # add param into a function
    # is array is always suppose to be false because we never allow arrays parameters
    # receives the function, the var name, type, its address, and whetever is an array or not
    def addParameter(self, func, name, tipo, direccion, isArray):
        func.appendParam(variable(name, tipo, direccion, isArray, -1))


    # add var into a function
    #receives a class func, a name, a type, an address, if it an array, and ist size
    def addVarFunc(self, func, name, tipo, direccion, isArray, arrSize = -1):
        func.appendVar(variable(name, tipo, direccion, isArray, arrSize, ), self)

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
                            '=' : 'int',
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
                            '=' : 'int',
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
                            '=' : 'err',
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
                            '==' : 'int',
                            '=' : 'int',
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
                            '=' : 'int',
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
                            '=' : 'err',
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
                            '=' : 'err',
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
                            '=' : 'err',
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
                            '=' : 'int',
                            '!=' : 'int',
                            '&&' : 'err',
                            '||' : 'err'
                        }
                }
    }

