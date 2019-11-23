from funcion import funcion
from variable import variable
from memory import memoria

class clase:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

        # public stuff
        self.publicMetodos = [] #lista de funciones
        self.publicAtributos = [] #lista de atributos

        # private stuff
        self.privateMetodos = [] # lista de funciones privadas
        self.privateAtributos = [] # lista de atributos privados


        self.memoriaGlobal = memoria(5000, 8000, 11000)


    def szEnteros():
        return self.memoriaGlobal.i

    def szFlotantes():
        return self.memoriaGlobal.f

    def szChars():
        return self.memoriaGlobal.c

    def getVariables(self):
        return len(self.privateAtributos) + len(self.publicAtributos)

    def appendFunction(self, funcA, isPublic):
        if isPublic:
            self.publicMetodos.append(funcA)
        else:
            self.privateMetodos.append(funcA)

    def appendAtributo(self, varA, isPublic):
        if isPublic:
            self.publicAtributos.append(varA)
        else:
            self.privateAtributos.append(varA)

    def getFunction(self, isPublic):
        if isPublic:
            return self.publicMetodos[len(self.publicMetodos)-1]
        else:
            return self.privateMetodos[len(self.publicMetodos)-1]

        
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


