import sys
import pickle
import copy
import mappingQuads

sizeMemory = 10000
initialOffset = 1000
localOffset = 3
constantOffset = 6
classOffset = 9
direcciones = [1000,11000,21000,31000,41000,51000,61000,71000,81000,91000,101000,111000,121000]
class VM: 
  def __init__(self):
    self.quadruples = []
    self.ip = [0]
    self.auxIp = 0

    self.offset = [(0, 'global')]
    self.dict_params = []
    self.global_memory = [[], [], []]
    self.local_memory = [[[], [], []]]
    self.constant_memory = [[], [], []]
    self.class_global_memory = [[], [], []]

  def get_type(self, direccion):
    #print(direccion)
    for i in range(len(direcciones) - 1):
      if (direccion >= direcciones[i] and direccion < direcciones[i+1]):
        result = i%3
        if (result == 0):
          return "int"
        elif (result == 1):
          return "float"
        else:
          return "char"

  def get_default_type(self, direccion):
    tipo = self.get_type(direccion)
    if (tipo == "int"):
      return 0
    elif (tipo == "float"):
      return 0.0
    else:
      return ' '

  def convert_both(self, left, right):
    # convert left and right operands
    return [self.convert_left(left),self.convert_right(right)]

  def convert_left(self, left):
    left_operand = self.get_value(left)
    return left_operand

  def convert_right(self, right):
    right_operand = self.get_value(right)
    return right_operand

  def doOffset(self, direccion):
    if (self.get_memory_type(direccion) == "global" or self.get_memory_type(direccion) == "constant" or self.get_memory_type(direccion) == "local"):
      return direccion
    desplazo = self.offset[len(self.offset)-1][0]
    return desplazo + direccion

  def notAssignment(self, quad):
      if quad == mappingQuads.CC_I or quad==mappingQuads.CF_I or quad==mappingQuads.CI_I or quad==mappingQuads.ERA_I or quad==mappingQuads.SET_I or quad==mappingQuads.GOSUB_I or quad==mappingQuads.GOTOF_I or quad==mappingQuads.SUM_ADDRESS_SET_I:
          return False
      return True


  # Main execution of the quadruples
  def execute(self, quads):
    self.read_quadruples(quads)
    while(self.ip[len(self.ip)-1] != len(self.quadruples)):

#      print(self.ip[len(self.ip)-1])   
      current_quad = self.quadruples[self.ip[len(self.ip)-1]]
      tmpQuad = copy.copy(current_quad)
      changed = False
      for i in range(3):
          if(current_quad[i+1] and self.notAssignment(current_quad[0]) and current_quad[i+1] < 0 ):
              changed = True
              current_quad[i+1] = self.get_value(-current_quad[i+1])
        
  #    print(current_quad)
 #     print(self.class_global_memory, " / ",  self.global_memory, " / ", self.local_memory, " / ", self.offset)
      #print(self.offset)

      # Start mapping of operationso
      if current_quad[0] == mappingQuads.NEGATE_I:
          right = self.convert_right(current_quad[2])
          self.set_value(current_quad[3], -right)
      elif current_quad[0] == mappingQuads.NOT_I:
          right = self.convert_right(current_quad[2])
          self.set_value(current_quad[3], not right)
      elif current_quad[0] == mappingQuads.SUM_ADDRESS_SET_I:
          if self.get_memory_type(current_quad[2]) != "global":
            right = int(current_quad[2])
            right = right + int(self.offset[len(self.offset)-1][0])
            self.set_value(current_quad[3], right)
          else:
            right = int(current_quad[2])
            self.set_value(current_quad[3], right)


      elif current_quad[0] == mappingQuads.UNSET_I:
        self.offset.pop()

      elif current_quad[0] == mappingQuads.READ_I:
        x = input()
        self.set_value(current_quad[3], x)

      elif current_quad[0] == mappingQuads.MAS_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand + right_operand)

      elif current_quad[0] == mappingQuads.MENOS_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand - right_operand)

      elif current_quad[0] == mappingQuads.MULT_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand * right_operand)

      elif current_quad[0] == mappingQuads.DIV_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        if (right_operand == 0):
          raise ZeroDivisionError("PPC - Cannot divide by 0 value")
        if (self.get_type(current_quad[1]) == "int" and self.get_type(current_quad[2]) == "int"):
          self.set_value(current_quad[3], left_operand // right_operand)
        else:
          self.set_value(current_quad[3], left_operand / right_operand)

      elif current_quad[0] == mappingQuads.AND_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand and right_operand)

      elif current_quad[0] == mappingQuads.OR_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand or right_operand)

      elif current_quad[0] == mappingQuads.DIFERENTE_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand != right_operand)

      elif current_quad[0] == mappingQuads.IGUALQUE_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand == right_operand)

      elif current_quad[0] == mappingQuads.MAYOR_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand > right_operand)

      elif current_quad[0] == mappingQuads.MAYORIGUAL_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand >= right_operand)

      elif current_quad[0] == mappingQuads.MENOR_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand < right_operand)

      elif current_quad[0] == mappingQuads.MENORIGUAL_I:
        left = self.doOffset(current_quad[1])
        right = self.doOffset(current_quad[2])
        [left_operand, right_operand] = self.convert_both(left, right)
        self.set_value(current_quad[3], left_operand <= right_operand)

      elif current_quad[0] == mappingQuads.GOTO_I:
        self.ip[len(self.ip)-1] = current_quad[3] - 1

      elif current_quad[0] == mappingQuads.GOTOF_I:
        left_operand = self.convert_left(current_quad[1])
        if not left_operand:
          self.ip[len(self.ip)-1] = current_quad[3] - 1

      elif current_quad[0] == mappingQuads.PARAM_I:
        left = self.doOffset(current_quad[1])
        left_operand = self.convert_left(left)
        self.dict_params.append((current_quad[3], left_operand))

      elif current_quad[0] == mappingQuads.ERA_I:
        pass

      elif current_quad[0] == mappingQuads.GOSUB_I:
        self.ip.append(current_quad[3] - 1)
        self.local_memory.append([[], [], []])
        for val in self.dict_params:
          self.set_value(val[0], val[1])
        self.dict_params = []

      elif current_quad[0] == mappingQuads.ENDPROC_I:
        # get previous ip
        self.ip.pop()
        #clear local memory
        self.local_memory.pop()
        # clear params
        self.params = {}
        self.ip[len(self.ip)-1] = self.ip[len(self.ip)-1]          

      elif current_quad[0] == mappingQuads.CI_I:
        self.set_value(current_quad[3], int(current_quad[2]))

      elif current_quad[0] == mappingQuads.CF_I:
        self.set_value(current_quad[3], float(current_quad[2]))

      elif current_quad[0] == mappingQuads.CC_I:
        self.set_value(current_quad[3], current_quad[2])

      elif current_quad[0] == mappingQuads.PRINT_I:
          tmpDir = current_quad[3]
          tmpDir = self.doOffset(tmpDir)
          val = str(self.get_value(tmpDir))
          
          if val[0] == "'":
            val = val[1:len(val)-1]  
            if(val == "\\n"):
                sys.stdout.write('\n')
            elif(val =="\\t"):
                sys.stdout.write('\t')
            else:
                sys.stdout.write(val)
          else:
            sys.stdout.write(val)

      elif current_quad[0] == mappingQuads.VALID_I:
        try:
          left_operand = int(current_quad[1])
          right_operand = int(current_quad[2])
          index = self.get_value(current_quad[3])
          if (index < left_operand or index >= right_operand):
            raise Exception()
        except:
          raise IndexError(f"PPC The index {index} is out of range")
      elif current_quad[0] == mappingQuads.SUM_VAL_ADDRESS_I:
        left = self.doOffset(current_quad[1])
        left_operand = self.convert_left(left)
        self.set_value(current_quad[3], (left_operand + int(current_quad[2])))

      elif current_quad[0] == mappingQuads.IGUAL_I:
        right = self.doOffset(current_quad[2])
        right_operand = self.convert_right(right)
     #   print(right_operand)
        typeOp = self.get_type(current_quad[2])
        if (typeOp == "float"):
          right_operand = float(right_operand)
        elif (typeOp == "int"):
          right_operand = int(right_operand)
        #print(current_quad[3], right_operand)
        self.set_value(current_quad[3], right_operand)

      elif current_quad[0] == mappingQuads.SET_I:
        # right_operand = str(current_quad[2])
        # if self.offset[len(self.offset)-1][1] != right_operand:
        #   self.offset.append((self.offset[len(self.offset)-1][0]+current_quad[3], right_operand))
        # else:
        #   self.offset.append((self.offset[len(self.offset)-1][0], right_operand))

         self.offset.append((self.offset[len(self.offset)-1][0]+current_quad[3], ""))
      else:
        raise KeyError(f"PPC {current_quad[0]} is not handled")
      
      if changed:
      #dont delete this
          self.quadruples[self.ip[len(self.ip)-1]] = tmpQuad


      #next quad
      self.ip[len(self.ip)-1] = self.ip[len(self.ip)-1]+1 
      
      # Keep adding quads

  def read_quadruples(self, quads):
    with open(quads, 'rb') as file:
      self.quadruples = pickle.load(file)

  def get_value(self, direccion):
    if (direccion < 0):
       return self.get_value(direccion*-1)
    #print(direccion)
    memory_type = self.get_memory_type(direccion)
    self.generateChunkMemory(direccion)
    if (memory_type == "global"):
      return self.global_memory[direccion//sizeMemory][direccion%sizeMemory-initialOffset]
    elif (memory_type == "local"):
      return self.local_memory[len(self.local_memory)-1][direccion//sizeMemory-localOffset][direccion%sizeMemory-initialOffset]
    elif (memory_type == "constant"):
      return self.constant_memory[direccion//sizeMemory - constantOffset][direccion%sizeMemory-initialOffset]  
    elif (memory_type == "class"):
      return self.class_global_memory[direccion//sizeMemory - classOffset][direccion%sizeMemory-initialOffset]

  def set_value(self, direccion, value):
    direccion = int(direccion)
    if (direccion < 0):
       return self.set_value(self.get_value(direccion*-1), value)
    self.generateChunkMemory(direccion)
    memory_type = self.get_memory_type(direccion)
    tipo = self.get_type(direccion)
    newValue = -1
    try:
      if (tipo == "int"):
        newValue = int(value)
      elif (tipo == "float"):
        newValue = float(value)
      elif (tipo == "char"):
        if (type(value) == str and len(value) >= 1):
          newValue = value
        else:
          raise Exception
    except:
      raise ValueError(f"PPC - Failed at parsing value={value}")

    if (memory_type == "global"):
      self.global_memory[direccion//sizeMemory][direccion%sizeMemory-initialOffset] = newValue
    elif (memory_type == "local"):
      self.local_memory[len(self.local_memory)-1][direccion//sizeMemory-localOffset][direccion%sizeMemory-initialOffset] = newValue
    elif (memory_type == "constant"):
      self.constant_memory[direccion//sizeMemory - constantOffset][direccion%sizeMemory-initialOffset] = newValue
    elif (memory_type == "class"):
      self.class_global_memory[direccion//sizeMemory - classOffset][direccion%sizeMemory-initialOffset] = newValue
      
  def generateChunkMemory(self, direccion):
    direccion = int(direccion)
  #  print(direccion)
    memory_type = self.get_memory_type(direccion)
    default = self.get_default_type(direccion)
    if (memory_type == "global"):
      while len(self.global_memory[direccion//sizeMemory]) < direccion%sizeMemory-initialOffset+1:
        self.global_memory[direccion//sizeMemory].append(default)
    elif (memory_type == "local"):
      while len(self.local_memory[len(self.local_memory)-1][direccion//sizeMemory-localOffset]) < direccion%sizeMemory-initialOffset+1:
        self.local_memory[len(self.local_memory)-1][direccion//sizeMemory-localOffset].append(default)
    elif (memory_type == "constant"):
      while(len(self.constant_memory[direccion//sizeMemory-constantOffset]) < direccion%sizeMemory-initialOffset+1):
        self.constant_memory[direccion//sizeMemory-constantOffset].append(default)
    elif (memory_type == "class"):
      while(len(self.class_global_memory[direccion//sizeMemory-classOffset]) < direccion%sizeMemory-initialOffset+1):
        self.class_global_memory[direccion//sizeMemory-classOffset].append(default)


  def get_memory_type(self, direccion):
    if (direccion < direcciones[3]):
      return "global"
    elif (direccion < direcciones[6]):
      return "local"
    elif (direccion < direcciones[9]):
      return "constant"
    elif (direccion < direcciones[12]):
      return "class"

def main(argv):
  program = VM()
  program.execute(argv[1])

if __name__ == '__main__':
  main(sys.argv)

