class EquationInfo():
  def __init__(self):
    self.order = 1
    self.variables = set()
    self.hasGrad = False
    self.hasLaplace = False
    self.gradVar = set()
    self.laplaceVar = set()
  
  def __str__(self):
    res = f"order : {self.order}\n"
    res += f"grad : {self.hasGrad}\n"
    res += f"laplace : {self.hasLaplace}\n"
    res += f"variables : {list(self.variables)}\n"
    res += f"gradVar : {list(self.gradVar)}\n"
    res += f"laplaceVar : {list(self.laplaceVar)}"
    return res
  
  def __repr__(self) -> str:
    return self.__str__()