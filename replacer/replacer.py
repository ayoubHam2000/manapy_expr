from typing import  Match, List
import re

class CreateEquation:
  def __init__(self, query : str, order : int, dimension : int):
    self.query = query
    self.order = order
    self.dimension = dimension
  

  def __str__(self) :
    return f"equation {self.query} order => {self.order} dimension => {self.dimension}"

  def compile(self):
    pass


class CreateSystem():

  def __init__(self, path : str, equations : List[CreateEquation]):
    self.path = path
    self.equations = equations
    self.device = "cpu"
    self.backend = "python"
    self.target_template = "./templates/advecdiff.py"
    self.process_token = self.__get_process_token()

  def using(self, device : str, backend : str):
    self.device = device
    self.backend = backend
    return self
  
  def generate(self):
    with open(self.target_template) as file:
      data = file.read()
      pattern = r'\$\$\[(.*?)\]'
      result = re.sub(pattern, self.__replace_with, data)
      with open(self.path, "w") as out_file:
        out_file.write(result)
  
  ##########################################
  ## Replacer
  ##########################################
  """
  Replacer
  """
  def __get_process_token(self):
    return {
      "backend" : self.__dimension_replace
    }
  
  def __dimension_replace(self):
    res = f"Backend is {self.backend} device is {self.device} equations\n"
    for eq in self.equations:
      res += str(eq) + "\n"
    return res

  def __replace_with(self, match : Match[str]):
    matched_value = match.group(1)
    if matched_value in self.process_token:
      return self.process_token[matched_value]()
    return ""



path = "./out/out_file.py"
q1 = CreateEquation("delta.u + v = 0", order=1, dimension=2)
s = CreateSystem(path, [
  q1
]).using(device="cpu", backend="numba").generate()
