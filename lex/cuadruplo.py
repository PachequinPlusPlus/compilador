class cuadruplo:
    #op, left and right are integers
    def __init__(self, op, left, right, result):
        self.op = op
        self.left = left
        self.right = right
        self.result = result

    def convert(self, val):
        if val == None:
            return "None"
        return val

    def imprimirCuadruplo(self, directory, ind, toConsole):
        quad = open(directory, 'a')
        myquad = f"{self.convert(ind):>04} : {self.convert(self.op):>15} {self.convert(self.left):>10} {self.convert(self.right):>10} {self.convert(self.result):>10}"
        if toConsole:
            print(myquad)
        quad.write(myquad)
        quad.write('\n')
        quad.close()
