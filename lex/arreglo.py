class arreglo:
    def __init__(self, up):
        self.up = up 

    def getSize(self):
        return self.up

    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)
