class Operation():
  Laplace = 0
  Grad = 1
  Dx = 2
  Dy = 3
  Dz = 4
  Dt = 5
  Mul = 6
  Add = 7
  
  nb_operations = 12

  def __init__(self, opType : int):
    m = ["Laplace", "Grad", "Dx", "Dy", "Dz", "Dt", "Mul", "Add"]
    self.name = m[opType]
    self.type = opType
    self.order = 1
  
  def augment_order(self):
    self.order += 1
    self.name += str(self.order)

  def __str__(self):
    if self.order == 1:
      return f"OP[{self.name}]"
    else :
      return f"OP2[{self.name}]"
  
  def get_index(self):
    if self.type in [Operation.Dx, Operation.Dy, Operation.Dz, Operation.Dt] and self.order == 2:
      return self.type + 6
    return self.type