# nombre | direcion
class semantics:
    scopes = ["global"]
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


    def appendVariable(self, name):
        topScopes = self.scopes[len(self.scopes)-1]
        if len(self.funcs) == 0:
            self.classes.setdefault(topScopes, {}).setdefault("attr", []).append({"name" : name, "direccion" : 1000})

        else:
            topFuncs = self.funcs[len(self.funcs)-1]
            self.classes.setdefault(topScopes, {}).setdefault("metodos", {}).setdefault(topFuncs, {}).setdefault("attr", []).append({"name" : name, "direccion" : 1000})


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

