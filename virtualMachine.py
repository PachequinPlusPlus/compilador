import sys
import pickle
import mappingQuads

direcciones = [1000,11000,21000,31000,41000,51000,61000,71000,81000,91000,101000,111000,121000,131000,141000,151000]
sizeMemory = 10000
initialOffset = 1000
localOffset = 3
constantOffset = 6
classOffset = 9
class VM:
  def __init__(self):
    self.quadruples = []
    self.ip = [0]
    self.auxIp = 0

    self.dict_params = {}
    self.global_memory = [[], [], []]
    self.local_memory = [[[], [], []]]
    self.constant_memory = [[], [], []]

  def get_type(self, direccion):
    for i in range(direcciones)-1:
      if (direccion > direcciones[i] and direccion < direcciones[i+1]):
        result = i%3
        if (result == 0):
          return "int"
        elif (result == 1):
          return "float"
        else:
          return "char"

  def get_default_type(self, direccion):
    tipo = get_type(direccion)
    if (tipo == "int"):
      return 0
    elif (tipo == "float"):
      return 0.0
    else:
      return ''

  def convert_both(self, left, right):
    # convert left and right operands
    return [self.convert_left(left),self.convert_right(right)]

  def convert_left(self, left):
    left_operand = self.get_value(left)
    return left_operand

  def convert_right(self, right):
    right_operand = self.get_value(right)
    return right_operand

  # Main execution of the quadruples
  def execute(self, quads):
    self.read_quadruples(quads)
    while(self.ip[len(self.ip)] != len(self.quadruples)):
      current_quad = self.quadruples[self.ip]
      

      # Start mapping of operations
      if current_quad[0] == mappingQuads.MAS_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand + right_operand)
      elif current_quad[0] == mappingQuads.MENOS_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand - right_operand)
      elif current_quad[0] == mappingQuads.MULT_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand * right_operand)
      elif current_quad[0] == mappingQuads.DIV_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        if (right_operand == 0):
          raise ZeroDivisionError("Cannot divide by 0 value")
        if (self.get_type(current_quad[1]) == "int" and self.get_type(current_quad[2]) == "int"):
          self.set_value(current_quad[3], left_operand // right_operand)
        else:
          self.set_value(current_quad[3], left_operand / right_operand)
      elif current_quad[0] == mappingQuads.AND_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand and right_operand)
      elif current_quad[0] == mappingQuads.OR_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand or right_operand)
      elif current_quad[0] == mappingQuads.DIFERENTE_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand != right_operand)
      elif current_quad[0] == mappingQuads.IGUALQUE_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand == right_operand)
      elif current_quad[0] == mappingQuads.MAYOR_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand > right_operand)
      elif current_quad[0] == mappingQuads.MAYORIGUAL_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand >= right_operand)
      elif current_quad[0] == mappingQuads.MENOR_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand < right_operand)
      elif current_quad[0] == mappingQuads.MENORIGUAL_I:
        [left_operand, right_operand] = self.convert_both(current_quad[1], current_quad[2])
        self.set_value(current_quad[3], left_operand <= right_operand)
      elif current_quad[0] == mappingQuads.GOTO:
        self.ip[len(self.ip)] = current_quad[3] - 1
      elif current_quad[0] == mappingQuads.GOTOF:
        left_operand = convert_left(current_quad[1])
        if not left_operand:
          self.ip[len(self.ip)] = current_quad[3] - 1
      elif current_quad[0] == mappingQuads.PARAM_I:
        left_operand = convert_left(current_quad[1])
        self.dict_params[current_quad[3]] = self.get_value(left_operand)
      elif current_quad[0] == mappingQuads.GOSUB_I:
        self.ip.append(current_quad[3] - 1)
        self.local_memory.append([[], [], []])
        for key, value in self.dict_params:
          self.set_value(key, value)
      elif current_quad[0] == mappingQuads.ENDPROC_I:
        # get previous ip
        self.ip.pop()
        #clear local memory
        self.local_memory.pop()
        # clear params
        self.params = {}
      elif current_quad[0] == mappingQuads.CI_I:
        self.set_value(current_quad[3], int(current_quad[2]))
      elif current_quad[0] == mappingQuads.CF_I:
        self.set_value(current_quad[3], float(current_quad[2]))
      elif current_quad[0] == mappingQuads.CC_I:
        self.set_value(current_quad[3], str(current_quad[2]))
        # self.constant_memory[current_quad[3]/sizeMemory - constantOffset][current_quad[3]%sizeMemory-initialOffset] = str(current_quad[2])
      elif current_quad[0] == mappingQuads.PRINT_I:
        print(self.get_value(current_quad[3]), end='')
      elif current_quad[0] == mappingQuads.VALID_I:
        try:
          left_operand = int(current_quad[1])
          right_operand = int(current_quad[2])
          index = self.get_value(current_quad[3])
          if (index < left_operand or index >= right_operand):
            raise Exception()
        except:
          raise IndexError(f"The index {index} is out of range")
      elif current_quad[0] == mappingQuads.SUM_VAL_ADDRESS_I:
        left_operand = convert_left(current_quad[1])
        self.set_value(current_quad[3], left_operand + int(current_quad[2]))

      #next quad
      self.ip[len(self.ip)] = self.ip[len(self.ip)]+1 
      # Keep adding quads

  def read_quadruples(self, quads):
    with open(quads, 'rb') as file:
      self.quadruples = pickle.load(file)
      print(self.quadruples)

  def get_value(self, direccion):
    memory_type = self.get_memory_type(direccion)
    if (memory_type == "global"):
      return self.global_memory[direccion/sizeMemory][direccion%sizeMemory-initialOffset]
    elif (memory_type == "local"):
      return self.local_memory[len(self.local_memory)-1][direccion/sizeMemory-localOffset][direccion%sizeMemory-initialOffset]
    elif (memory_type == "char"):
      return self.constant_memory[direccion/sizeMemory - constantOffset][direccion%sizeMemory-initialOffset]  
    
  def set_value(self, direccion, value):
    self.generateChunkMemory(direccion)
    memory_type = self.get_memory_type(direccion)
    tipo = self.get_type(direccion)
    try:
      if (tipo == "int"):
        newValue = int(value)
      elif (tipo == "float"):
        newValue = float(value)
      elif (tipo == "char"):
        if (type(value) == str and len(value) == 1):
          newValue = value
        else:
          raise Exception()
    except:
      # TODO(CorrectError??)
      raise ValueError(f"Failed at parsing value={value}")

    if (memory_type == "global"):
      self.global_memory[direccion/sizeMemory][direccion%sizeMemory-initialOffset] = newValue
    elif (memory_type == "local"):
      self.local_memory[len(self.local_memory)-1][direccion/sizeMemory-localOffset][direccion%sizeMemory-initialOffset] = newValue
    elif (memory_type == "constant"):
      self.constant_memory[direccion/sizeMemory - constantOffset][direccion%sizeMemory-initialOffset] = newValue

  def generateChunkMemory(self, direccion):
    memory_type = self.get_memory_type(direccion) 
    default = self.get_default_type(direccion)
    if (memory_type == "global"):
      for _ in range(direccion%sizeMemory-initialOffset+1):
        self.global_memory[direccion/sizeMemory].append(default)
    elif (memory_type == "local"):
      for _ in range(direccion%sizeMemory-initialOffset+1):
        self.local_memory[len(self.local_memory)-1][direccion/sizeMemory-localOffset].append(default)
    elif (memory_type == "constant"):
      for _ in range(direccion%sizeMemory-initialOffset+1):
        self.constant_memory[direccion/sizeMemory-constantOffset].append(default)


  def get_memory_type(self, direccion):
    if (direccion < direcciones[3]):
      return "global"
    elif (direccion < direcciones[6]):
      return "local"
    else:
      return "constant"


def main(argv):
  program = VM()
  program.execute(argv[1])

if __name__ == '__main__':
  main(sys.argv)

