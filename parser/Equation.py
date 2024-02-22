from Symbol import Symbol

class Equation():
  def __init__(self, expr : Symbol, dim):
    if not isinstance(expr, Symbol):
      raise TypeError("expr must be of type Symbol")
    if dim != 1 and dim != 2:
      raise RuntimeError("dim must be of value 1 or 2")
    self.dim = dim
    self.expr = expr

    self.info = self.expr.getInfo(dim = self.dim)