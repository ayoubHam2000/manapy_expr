from Constant import Constant
from Variable import Variable
from Operation import Operation
from collections import deque
from Simplifier import simplify_tree
from EquationInfo import EquationInfo

class Node():

  def __init__(self, value, name = None):
    if isinstance(value, (int, float)):
      if name == None:
        name = str(round(value, 3))
      value = Constant(name, value)
    if isinstance(value, str):
      value = Variable(value)
    if not isinstance(value, (Operation, Variable, Constant)):
      raise TypeError(f"can't construct Node from {type(value)}")
    self.token = value
    self.right = None
    self.left = None

  """
    raise an error if we can't do any operations.
    return  True to add a new node, to have the new node point to self node
            False to alter self content
  """
  def __checkOperation(self, operation : Operation):
    if isinstance(self.token, Variable) :
      return False
    if isinstance(self.token, Operation) :
      if self.token.type == operation.type:
        if self.token.type in [Operation.Laplace, Operation.Grad]:
          raise RuntimeError("Laplace or Grad Can't be nested")
        elif self.token.type in [Operation.Dt, Operation.Dx, Operation.Dy, Operation.Dz] \
          and self.token.order > 1:
          raise RuntimeError("Max order of a variable is 2")
        self.token.augment_order()
        return True

    raise TypeError(f"operation can only perform on Variable type or Node with the same operation type")

  def __addOperation(self, operation : Operation):
    exist = self.__checkOperation(operation)
    if not exist:
      res = Node(operation)
      res.left = self
      res.right = None
      return res
    else:
      return self

  def laplace(self):
    return self.__addOperation(Operation(Operation.Laplace))

  def grad(self):
    return self.__addOperation(Operation(Operation.Grad))

  def dx(self):
    return self.__addOperation(Operation(Operation.Dx))

  def dy(self):
    return self.__addOperation(Operation(Operation.Dy))
  
  def dz(self):
    return self.__addOperation(Operation(Operation.Dz))

  def dt(self):
    return self.__addOperation(Operation(Operation.Dt))

  def exec(self):
    if isinstance(self.token, Operation):
      if self.token.type == Operation.Add:
        return f"{self.left.exec()} + {self.right.exec()}"
      elif self.token.type == Operation.Mul:
        return f"({self.left.exec()}) * ({self.right.exec()})"
      elif self.token.type == Operation.Dt:
        return f"Dt{self.token.order}({self.left.exec()})"
      elif self.token.type == Operation.Dx:
        return f"Dx{self.token.order}({self.left.exec()})"
      elif self.token.type == Operation.Dy:
        return f"Dy{self.token.order}({self.left.exec()})"
      elif self.token.type == Operation.Dz:
        return f"Dz{self.token.order}({self.left.exec()})"
      elif self.token.type == Operation.Laplace:
        return f"Laplace({self.left.exec()})"
      elif self.token.type == Operation.Grad:
        return f"Grad({self.left.exec()})"
    elif isinstance(self.token, (Variable, Constant)):
      return self.token.name
    return ""
  
  def expand(self):
    if isinstance(self.token, Operation):
      if self.token.type == Operation.Add:
        return self.left.expand() + self.right.expand()
      elif self.token.type == Operation.Mul:
        a = self.left.expand()
        b = self.right.expand()
        res = []
        for i in a:
          for j in b:
            z = i + j
            res.append(z)
        return res
    return [[self]]
  
  def getInfo(self, dim):
    res = EquationInfo()
    if dim == 1 or dim == 2:
      arr = self.expand()
      for add in arr:
        for mul in add:
          if isinstance(mul.token, Variable):
            res.variables.add(mul)
          elif isinstance(mul.token, Operation):
            op = mul.token
            res.order = max(op.order, res.order)
            if op.type == Operation.Grad:
              res.hasGrad = True
              res.gradVar.add(mul.left)
            if op.type == Operation.Laplace:
              res.hasLaplace = True
              res.order = 2
              res.laplaceVar.add(mul.left)
            if op.type == Operation.Dz and dim == 1:
              raise RuntimeError("Equation of order 1 can't have dz operation")
            res.variables.add(mul.left)
    return res

  """
    Return a simplified expression without factorization.
  """
  def reduce(self, dim):
    return simplify_tree(self, dim)

  """
   - if x = 1 or self.token = 1 constant, just return the node Ex: 1 * a = a, a * 1 = a, 1 * 1 = 1
   - 1/Avoid multiplication between operations such as (dx * dx), (dy * dx), or (dy * grad)
    - grad * grad | grad * laplace | laplace * laplace => possible for the same variable
   - 2/Prevent multiplication between variables and operations involving variables, such as dx(u) * v
   - 3/Avoid multiplication between different variables, such as v * u
  """
  def __mul__(self, x):
    if not isinstance(x, Node):
      x = Node(x)
    if isinstance(x.token, Constant) and x.token.value == 1:
      return self
    if isinstance(self.token, Constant) and self.token.value == 1:
      return x
    
    #####
    var1 = self
    if isinstance(self.token, Operation):
      var1 = self.left
    var2 = x
    if isinstance(x.token, Operation):
      var2 = x.left
    if var1 != var2 and isinstance(var1, Variable) and isinstance(var2, isinstance(var1, Variable)):
      raise RuntimeError("multiplication of different variables")
    
    ######
    if isinstance(self.token, Operation) and isinstance(x.token, Operation):
      not_allowed = [Operation.Dx, Operation.Dy, Operation.Dz, Operation.Dt]
      if self.token.type in not_allowed or x.token.type in not_allowed:
        raise RuntimeError("can't do multiplication between partial operations")
    
    #####
    if isinstance(self.token, Operation) and isinstance(x.token, Variable) or \
      isinstance(self.token, Variable) and isinstance(x.token, Operation) or \
      isinstance(self.token, Variable) and isinstance(x.token, Variable):
      raise RuntimeError("can't do multiplication between variables or operation of variable")

    res = Node(Operation(Operation.Mul))
    res.left = self
    res.right = x
    return res

  def __rmul__(self, x):
    x = Node(x)
    return x * self

  def __add__(self, x):
    if not isinstance(x, Node):
      x = Node(x)
    res = Node(Operation(Operation.Add))
    res.left = self
    res.right = x
    return res

  def __radd__(self, x):
    x = Node(x)
    return x + self

  # region Printing
    ##########################################
    ## Printing
    ##########################################


  def __print_item_in_center(self, item : str, size : int):
    if len(item) > size:
      print(item[:size], end='.')
    else:
      nb_space = (size - len(item)) // 2
      print(' ' * nb_space, end='')
      print(item, end='')
      print(' ' * (size - nb_space - len(item)), end='')
  
  def __print_branch(self, size : int):
    nb = size // 4
    print(' ' * nb, end='')
    print('╭', end='')
    i = nb + 1
    while i + nb + 2 < size:
      if (i == (size - 1) // 2):
        print("┴", end='')
      else:
        print("─", end='')
      i += 1
    print('╮', end='')
    print(' ' * (size - (i + 1)), end='')
  
  def __print_tree(self, tree_height : int):
    level_item = tree_height
    item_len = 3
    buffer_size = pow(2, level_item) * item_len

    level = 1
    depth = 0
    level_type = 1
    level_item = 1

    queue = deque()
    is_empty_node = deque()

    queue.append(self)
    while depth < tree_height:
      if (level_type == 1):
        node = queue.popleft()
        if node :
          self.__print_item_in_center(str(node.token), buffer_size)
          queue.append(node.left)
          queue.append(node.right)
          is_empty_node.append(True)
        else :
          queue.append(None)
          queue.append(None)
          self.__print_item_in_center(" ", buffer_size)
          is_empty_node.append(False)
        level_item -= 1
        if (level_item == 0) :
          level_type = 2
          level_item = level
          level *= 2
          depth += 1
          print()
      else :
        while level_item != 0:
          is_empty = is_empty_node.popleft()
          if is_empty:
            self.__print_branch(buffer_size)
          else:
            self.__print_item_in_center(" ", buffer_size)
          level_item -= 1
        level_item = level
        level_type = 1
        buffer_size //= 2
        print()

  def tree_height(self, node):
      if node is None:
          return -1
      left_height = self.tree_height(node.left)
      right_height = self.tree_height(node.right)
      return 1 + max(left_height, right_height)

  # endregion

  def print(self):
    h = self.tree_height(self) + 1
    self.__print_tree(h)
  
  def __str__(self):
    return str(self.token)
  
  def __repr__(self):
    return str(self.token.name)