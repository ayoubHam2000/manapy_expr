from Node import Node
import re

class Symbol():
  symbolsDic = {}

  @staticmethod
  def symbols(s : str):
    res = []
    pattern = r'^[a-zA-Z ]*$'
    valid = bool(re.match(pattern, s))
    if not valid:
      raise RuntimeError("invalid input")
    tokens = s.split(' ')
    for t in tokens:
      if t not in Symbol.symbolsDic:
        Symbol.symbolsDic[t] = Symbol(t).node
      v = Symbol(Symbol.symbolsDic[t])
      res.append(v)
    return tuple(res)

  def __init__(self, value, name : str = None):
    if not (isinstance(value, (str, int, float, Node))):
      raise TypeError("Type error expect str, int, or float")
    if name != None and not isinstance(name, str):
      raise TypeError("Type error name must be string")
    if isinstance(value, Node):
      self.node = value
    else:
      if isinstance(value, str) and value in Symbol.symbolsDic:
        self.node = Symbol.symbolsDic[value]
      else:
        self.node = Node(value, name)
  
  def laplace(self):
    return Symbol(self.node.laplace())

  def grad(self):
    return Symbol(self.node.grad())

  def dx(self):
    return Symbol(self.node.dx())

  def dy(self):
    return Symbol(self.node.dy())
  
  def dz(self):
    return Symbol(self.node.dz())

  def dt(self):
    return Symbol(self.node.dt())
  
  def print(self):
    self.node.print()
  
  def exec(self):
    return self.node.exec()
  
  def reduce(self, dim):
    return Symbol(self.node.reduce(dim))
  
  def getInfo(self, dim):
    return self.node.getInfo(dim)

  def __mul__(self, x):
    if not isinstance(x, Symbol):
      x = Symbol(x)
    return Symbol(self.node * x.node)

  def __add__(self, x):
    if not isinstance(x, Symbol):
      x = Symbol(x)
    return Symbol(self.node + x.node)

  # 3 + Symbol => Symbol(3) + Symbol
  def __rmul__(self, x):
    x = Symbol(x)
    return x * self

  def __radd__(self, x):
    x = Symbol(x)
    return x + self
  
  def __str__(self):
    return str(self.node)
  
  def __repr__(self):
    return str(self.node.token.name)


def grad(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.grad()

def laplace(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.laplace()

def dx(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dx()

def dy(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dy()

def dz(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dz()

def dt(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dt()

def dx2(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dx().dx()

def dy2(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dy().dy()

def dz2(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dz().dz()

def dt2(s : Symbol):
  if not isinstance(s, Symbol):
    s = Symbol(s)
  return s.dt().dt()