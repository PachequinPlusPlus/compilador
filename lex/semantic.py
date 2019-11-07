from memory import myMemory
# nombre | direcion
class semantics:
    scopes = ["global"]
    types = []
    funcs = []

    def __init__(self):
        self.globales = myMemory(5000, 8000, 11000)
        self.locales = myMemory(14000, 17000, 19000)
        self.temporales = myMemory(25000, 27000, 29000)
        self.constantes = myMemory(30000, 30500, 31000)


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



    def checkFunctionExists(self, funcName):
        scope = self.tope(self.scopes)
        tmp = self.classes.get(scope).get("metodos").get(funcName)
        if tmp is not None:
            return True
        parent = self.classes.get(scope).get("parent")
        while parent is not None:
            tmp = self.classes.get(parent).get("metodos").get(funcName)
            if tmp is not None:
                return True
            parent = self.classes.get(parent).get("parent")

        return False
        

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


        

    # TODO(que matche los parametros)
    def deepLookingFunction(self, funcName, varName):
        scope = self.tope(self.scopes)
        self.setDefaultFunction(funcName)

        tmp = self.classes.get(scope).get("metodos").get(funcName).get("attr")
        for elem in tmp:
            if elem["name"] == varName:
                return elem 

        tmp = self.classes.get(scope).get("attr")
        for elem in tmp:
            if elem["name"] == varName:
                return elem

        parent = self.classes.get(scope).get("parent")

        while parent != None:
            tmp = self.classes.get(parent).get("attr")
            for elem in tmp:
                if elem["name"] == varName:
                    return elem
            parent = self.classes.get(parent).get("parent")
        return None

    

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
                            '*' : 'float'
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

