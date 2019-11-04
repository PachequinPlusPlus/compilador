class myMemory:

    def __init__(self, enteras, flotantes, chars):
        self.enteras = enteras
        self.flotantes = flotantes
        self.chars = chars
        self.i = 0
        self.f = 0
        self.c = 0

    def getEntera(self):
        self.i = self.i+1
        return self.enteras + self.i - 1

    def getFlotante(self):
        self.f = self.f+1
        return self.flotantes + self.f-1

    def getChar(self):
        self.c = self.c + 1
        return self.chars + self.c - 1

