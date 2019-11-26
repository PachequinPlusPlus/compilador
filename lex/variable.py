from arreglo import arreglo
class variable:
    def __init__(self, name, tipo, direccion, isArray, size):
        self.name = name
        self.tipo = tipo
        self.direccion = direccion
        self.isArray = isArray
        self.array = None
        # es una instanci

        if self.isArray:
            self.array = arreglo(size)

    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)
