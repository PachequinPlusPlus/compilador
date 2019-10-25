# nombre | direcion
class semantics:
    scopes = ["global"]
    types = []
    funcs = []

    direcionesGlobales = [1000, 2000, 3000]
    direccionesLocales = [4000, 5000, 6000]
    direccionesTemporales = [7000, 8000, 9000]

    classes = {
                "global" : {
                    "attr" : [],
                    "metodos" : {
                          "main" : {
                              "attr" : [],
                              "tipo" : "void"
                           }
                    },
                    "parent" : None
                    }
            }



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

        self.classes.setdefault(scope, {}).setdefault("metodos", {}).setdefault(funcName, {}).setdefault("attr", []).append({"name" : varName, "direccion" : 1000, "tipo" : tipo})

    def addAttrGlobal(self, varName, tipo):
        scope = self.tope(self.scopes)

        self.classes.setdefault(scope, {}).setdefault("attr", []).append({"name" : varName, "direccion" : 1000, "tipo" : tipo})

        


    def appendVariable(self, name):
        topScopes = self.scopes[len(self.scopes)-1]
        parent = "global"

        #TODO(ADD TIPOS)
        tipo = None #self.types[len(self.scopes)-1]

        if len(self.funcs) == 0:
            self.classes.setdefault(topScopes, {}).setdefault("attr", []).append({"name" : name, "direccion" : 1000, "tipo" : tipo})
        else:
            topFuncs = self.funcs[len(self.funcs)-1]
            self.classes.setdefault(topScopes, {}).setdefault("metodos", {}).setdefault(topFuncs, {}).setdefault("attr", []).append({"name" : name, "direccion" : 1000, "tipo" : tipo})
            
        self.classes[topScopes].setdefault("parent", parent)


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
                            '*' : 'int'
                        },
                    'float' : {
                            '+' : 'float',
                            '-' : 'float',
                            '/' : 'float',
                            '*' : 'float'
                        },
                    'char' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err'
                        }
                },
            'float' : {
                    'int' : {
                            '+' : 'float',
                            '-' : 'float',
                            '/' : 'float',
                            '*' : 'float'
                        },
                    'float' : {
                            '+' : 'float',
                            '-' : 'float',
                            '/' : 'float',
                            '*' : 'float'
                        },
                    'char' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err'
                        }
                },
            'char' : {
                    'int' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err'
                        },
                    'float' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err'
                        },
                    'char' : {
                            '+' : 'err',
                            '-' : 'err',
                            '/' : 'err',
                            '*' : 'err'
                        }
                }
    }

