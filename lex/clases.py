from funcion import funcion
from variable import variable
from memory import memoria

class clase:

    contador = [0]

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

        # public stuff
        self.publicMetodos = [] #lista de funciones
        self.publicAtributos = [] #lista de atributos

        # private stuff
        self.privateMetodos = [] # lista de funciones privadas
        self.privateAtributos = [] # lista de atributos privados


        # tratar memoria virtual
        if name != 'global':
            self.memoriaGlobal = memoria(91000, 101000, 111000)
            self.offSet = self.contador[0]
            self.contador[0] = self.contador[0] + 1
        else:
            self.memoriaGlobal = memoria(1000, 11000, 21000)
            self.offSet = 0




        #size
        self.size = 0


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

    def appendAtributo(self, varA, isPublic, semantica):
        # update size
        if varA.tipo == 'int' or varA.tipo == 'char' or varA.tipo == 'float':
            self.size = self.size + 1
        else:
            # var A es una clase
            varA.direccion = self.size
            self.size = semantica.getClase(varA.tipo).size + self.size

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


