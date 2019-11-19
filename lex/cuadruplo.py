class cuadruplo:
    #op, left and right are integers
    def __init__(self, op, left, right, result):
        self.op = op
        self.left = left
        self.right = right
        self.result = result


    def imprimirCuadruplo(self, directory, ind, toConsole):
        quad = open(directory, 'a')
        myquad = f"{ind:04} : {self.op:10} {self.left:10} {self.right:10} {self.result:10}"
        if toConsole:
            print(myquad)
        quad.write(myquad)
        quad.write('\n')
        quad.close()
