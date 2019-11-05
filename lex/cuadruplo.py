class cuadruplo:
    #op, left and right are integers
    def __init__(self, op, left, right, result):
        self.op = op
        self.left = left
        self.right = right
        self.result = result


    def imprimirCuadruplo(self):
        print(""+str(self.op)+"\t\t|\t\t\t"+str(self.left)+"\t\t\t|\t\t\t"+str(self.right)+"\t\t|\t\t\t"+str(self.result))
