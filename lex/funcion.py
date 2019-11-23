from variable import variable
from memory import memoria
class funcion:
    def __init__(self, name, tipoRetorno, ip):
        self.name = name
        self.tipoRetorno = tipoRetorno
        self.numberParams = 0
        self.params = [] # lista de variables de parametros
        self.vars = [] # lista de variables declarados
        # local memory for this scope
        # will be handled by the virtual machine
                            # enteros, float, char, clases
        self.memory = memoria(15000, 17000, 19000)
        self.ip = ip;

        
    
    def appendParam(self, varA):
        self.numberParams = self.numberParams + 1
        self.params.append(varA)

    def appendVar(self, varA):
        self.vars.append(varA)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
