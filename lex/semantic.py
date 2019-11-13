from memory import myMemory
from variable import variable
from clases import clase
from funcion import funcion

import json

# nombre | direcion
class semantics:
    scopes = ["global"]
    types = []
    funcs = []


    def __init__(self):
        self.clases = []


        self.globales = myMemory(5000, 8000, 11000)
        self.locales = myMemory(14000, 17000, 19000)
        self.temporales = myMemory(25000, 27000, 29000)
        self.constantes = myMemory(30000, 30500, 31000)

    def pr(self):
        parsed =str(self.clases).replace("'", '"')
        parsed = parsed.replace("False", 'false')
        parsed = parsed.replace("True", 'true')
        parsed = parsed.replace("None", '"None"')
        parsed2 = json.loads(parsed)
        #print(json.dumps(parsed2, indent=4))


    classes = {
                "global" : {
                    "attr" : [],
                    "metodos" : {
                          "main" : {
                              "attr" : [],
                              "tipo" : "void",
                              "params" : 0,
                              "isArray" : False,
                              "size" : 0
                           }
                    },
                    "parent" : None
                    }
            }


    #TODO(correguir las address temporales)
    def getAddress(self, tipo, isTemp = False):
        #TODO(que hacer para las clases?)
        scope = self.tope(self.scopes)
        if isTemp:
            if tipo == "int":
                return self.temporales.getEntera()
            elif tipo == "float":
                return self.temporales.getFlotante()
            elif tipo == "char":
                return self.temporales.getChar() 
 
        if scope == "global":
            if tipo == "int":
                return self.globales.getEntera()
            elif tipo == "float":
                return self.globales.getFlotante()
            elif tipo == "char":
                return self.globales.getChar() 
        else: 
            if tipo == "int":
                return self.locales.getEntera()
            elif tipo == "float":
                return self.locales.getFlotante()
            elif tipo == "char":
                return self.locales.getChar()


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


       

    def setDefaultFunction(self, funcName):
        scope = self.tope(self.scopes)
        self.classes.setdefault(scope, {}).setdefault("metodos", {}).setdefault(funcName, {}).setdefault("attr", [])

    def existInFunction(self, funcName, varName):
        scope = self.tope(self.scopes)
        self.setDefaultFunction(funcName)

        tmp = self.classes.get(scope).get("metodos").get(funcName).get("attr")
        for elem in tmp:
            if elem["name"] == varName:
                return True

       # tmp = self.classes.get(scope).get("attr")
       # for elem in tmp:
       #     if elem["name"] == varName:
       #         return True

      #  parent = self.classes.get(scope).get("parent")

#        while parent != None:
#            tmp = self.classes.get(parent).get("attr")
#            for elem in tmp:
#                if elem["name"] == varName:
#                    return True
#            parent = self.classes.get(parent).get("parent")

        return False

    def setDefault(self, scope):
        self.classes.setdefault(scope, {}).setdefault("attr", [])

    def exists(self, varName):
        scope = self.tope(self.scopes)
        # set the default for the actual scope
#        while scope != None:
        self.setDefault(scope)
        tmp = self.classes.get(scope).get("attr")
        for elem in tmp:
            if elem["name"] == varName:
                return True
        return False


    def updateNumberParams(self, funcName, numberParams):
        scope = self.tope(self.scopes)
        self.classes.get(scope).get("metodos").get(funcName).setdefault("params", 0)
        self.classes.get(scope).get("metodos").get(funcName)["params"] = numberParams

    def updateReturnType(self, funcName, returnType):
        scope = self.tope(self.scopes)
        self.classes.get(scope).get("metodos").get(funcName).setdefault("tipo", 'void')
        self.classes.get(scope).get("metodos").get(funcName)["tipo"] = returnType
        if returnType != 'void':
            self.addAttrFunction(funcName, "_"+funcName, returnType)



    

    def deepLookingRest(self, varName):
        scope = self.tope(self.scopes)
        self.setDefault(scope)

        tmp = self.classes.get(scope).get("attr")
        for elem in tmp:
            if elem["name"] == varName:
                return True

        parent = self.classes.get(scope).get("parent")

        while parent != None:
            tmp = self.classes.get(parent).get("attr")
            for elem in tmp:
                if elem["name"] == varName:
                    return True
            parent = self.classes.get(parent).get("parent")

        return False

    def tope(self, lista):
        if len(lista) == 0:
            return -1
        fr = lista[len(lista)-1]
        return fr

    def addMethod(self, name):
        clss = self.tope(self.scopes)
        self.classes.setdefault(clss, {}).setdefault("metodos", {})[name] = {}

    def addFunction(self, name):
        self.classes.setdefault("global", {})["metodos"][name] = {}

    # new functions
    #-------------------------------------------------------------------------------
    def appendClass(self, clase):
        self.clases.append(clase)

    def addClass(self, className, parent):
        self.clases.append(clase(className, parent))
        return self.tope(self.clases)

    # add a function into a class
    def addFunction(self, clase, isPublic, funcName, tipoRetorno):
        for cls in self.clases:
            if clase == cls:
                clase.appendFunction(funcion(funcName, tipoRetorno), isPublic)
                return clase.getFunction(isPublic)


    # add an attribute into a class
    def addAtributo(self, clase, varName, tipo, direccion, isArray, isPublic):
        clase.appendAtributo(variable(varName, tipo, direccion, isArray), isPublic)

    # add param into a function
    def addParameter(self, func, name, tipo, direccion, isArray):
        func.appendParam(variable(name, tipo, direccion, isArray))


    # add var into a function
    def addVarFunc(self, func, name, tipo, direccion, isArray):
        func.appendVar(variable(name, tipo, direccion, isArray))

    #-------------------------------------------------------------------------------





    def addAttrFunction(self, funcName, varName, tipo):
        scope = self.tope(self.scopes)
        addr = self.getAddress(tipo)

        self.classes.setdefault(scope, {}).setdefault("metodos", {}).setdefault(funcName, {}).setdefault("attr", []).append({"name" : varName, "direccion" : addr, "tipo" : tipo})

    def addAttrGlobal(self, varName, tipo):
        scope = self.tope(self.scopes)
        addr = self.getAddress(tipo)

        self.classes.setdefault(scope, {}).setdefault("attr", []).append({"name" : varName, "direccion" : addr, "tipo" : tipo})

        

    def appendType(self, tipo):
        self.types.append(tipo)

    def popType(self):
        self.types.pop()

    def appendParentForClasses(self, classe, parent):
        self.classes.setdefault(classe, {}).setdefault("parent", parent)

    def appendScope(self, scope):
        self.scopes.append(scope)

    def popScope(self):
        self.scopes.pop()

    def appendFuncs(self, funcName):
        self.funcs.append(funcName)

    def popFuncs(self):
        self.funcs.pop()

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

