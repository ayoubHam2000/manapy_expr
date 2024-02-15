from utils import get_math_symbol

class Constant():
  def __init__(self, name : str, value):
    self.name = get_math_symbol(name)
    self.value = value
  
  def __str__(self):
    return f"C[{self.name}]"