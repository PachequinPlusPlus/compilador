from variable import variable
class funcion:
    def __init__(self, name, tipoRetorno):
        self.name = name
        self.tipoRetorno = tipoRetorno
        self.numberParams = 0
        self.params = [] # lista de variables de parametros
        self.vars = [] # lista de variables declarados

    def appendParam(self, varA):
        self.numberParams = self.numberParams + 1
        self.params.append(varA)

    def appendVar(self, varA):
        self.vars.append(varA)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
