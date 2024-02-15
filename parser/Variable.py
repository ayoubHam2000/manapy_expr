from utils import get_math_symbol

class Variable():
  def __init__(self, name : str):
    self.name = get_math_symbol(name)
  
  def __str__(self):
    return f"V[{self.name}]"