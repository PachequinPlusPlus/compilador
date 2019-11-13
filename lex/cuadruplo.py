class cuadruplo:
    #op, left and right are integers
    def __init__(self, op, left, right, result):
        self.op = op
        self.left = left
        self.right = right
        self.result = result


    def imprimirCuadruplo(self, directory, ind):
        quad = open(directory, 'a')
        myquad = "{0:<4} : {1:<10} {2:<10} {3:<10} {4:<10}".format(str(ind), str(self.op), str(self.left), str(self.right), str(self.result))
        quad.write(myquad)
        quad.write('\n')
        quad.close()
