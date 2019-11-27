from variable import variable
from memory import memoria
class funcion:
    def __init__(self, name, tipoRetorno, ip):
        self.name = name
        self.tipoRetorno = tipoRetorno
        self.numberParams = 0
        self.params = [] # lista de variables de parametros
        self.vars = [] # lista de variables declarados
        self.size = 0
        # local memory for this scope
        # will be handled by the virtual machine
                            # enteros, float, char, clases
        self.memory = memoria(31000, 41000, 51000)
        self.ip = ip;

        # my class offset
        self.classOffset = 30000

        
    
    def appendParam(self, varA):
        self.numberParams = self.numberParams + 1
        self.params.append(varA)
        self.size = self.size + 1


    def appendVar(self, varA, semantica):
        if varA.tipo  == 'int' or varA.tipo == 'char' or varA.tipo == 'float':
            self.size = self.size + 1
        else:
            # var A es una clase
            print(varA.name, self.size)
            varA.direccion = self.size
            self.size = self.size + semantica.getClase(varA.tipo).size
            

        self.vars.append(varA)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
