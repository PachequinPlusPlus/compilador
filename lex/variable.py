class variable:
    def __init__(self, name, tipo, direccion, isArray):
        self.name = name
        self.tipo = tipo
        self.direccion = direccion
        self.isArray = isArray

    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)
