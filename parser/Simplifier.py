from Constant import Constant
from Variable import Variable
from Operation import Operation

"""
  return a tuple (a, b)
    a is dictionary has variable as a key and any array of Operation.nb_operations + 1
    [nb of variable a, nb of dx(a), nb of dy(a), ...]
    b is the sum of constant value
"""
def simplify_expression(expr):
  res = {}
  b = 0
  arr = expr.expand()
  for add in arr:
    val = 1
    var = None
    op = None
    for mul in add:
      if isinstance(mul.token, Constant):
        val *= mul.token.value
      elif isinstance(mul.token, (Variable)):
        var = mul
      elif isinstance(mul.token, (Operation)):
        var = mul.left
        op = mul.token
    if var == None:
      b += val
    else:
      if var not in res:
        res[var] = [0] * (Operation.nb_operations + 1)
      if op == None:
        res[var][0] += val
      else:
        res[var][op.get_index() + 1] += val
  return (res, b)

def simplify_for_op(arr, sub, to):
  items = [arr[i + 1] for i in sub]
  m = min(items)
  for i in sub:
    arr[i + 1] -= m
  arr[to] += m
  return arr

def simplify_for_grad(arr, dim):
  sub = [Operation.Dx, Operation.Dy, Operation.Dz]
  if dim == 1:
    sub = [Operation.Dx, Operation.Dy]
  return simplify_for_op(arr, sub, Operation.Grad + 1)

def simplify_for_laplace(arr, dim):
  sub = [Operation.Dx + 6, Operation.Dy + 6, Operation.Dz + 6]
  if dim == 1:
    sub = [Operation.Dx + 6, Operation.Dy + 6]
  return simplify_for_op(arr, sub, Operation.Laplace + 1)

"""
take the result of simplify_expression and construct a simplified tree.
  - Combine like terms, find grad and laplace 
"""
def to_tree(theTuple, dim):
  from Node import Node
  dic, v = theTuple

  tree = None

  tree_adder = lambda x : x if tree == None else tree + x

  if (v != 0):
    tree = tree_adder(Node(v))
    
  for item in dic:
    arr = dic[item]
    arr = simplify_for_grad(arr, dim)
    arr = simplify_for_laplace(arr, dim)
    for i in range(len(arr)):
      val = arr[i]
      if val != 0:
        val = Node(val)
        if i == 0:
          tree = tree_adder((val * item))
        elif i == Operation.Laplace + 1:
          tree = tree_adder((val * item.laplace()))
        elif i == Operation.Grad + 1:
          tree = tree_adder((val * item.grad()))
        elif i == Operation.Dx + 1:
          tree = tree_adder((val * item.dx()))
        elif i == Operation.Dy + 1:
          tree = tree_adder((val * item.dy()))
        elif i == Operation.Dz + 1:
          tree = tree_adder((val * item.dz()))
        elif i == Operation.Dt + 1:
          tree = tree_adder((val * item.dt()))
        elif i == Operation.Dx + 7:
          tree = tree_adder((val * item.dx().dx()))
        elif i == Operation.Dy + 7:
          tree = tree_adder((val * item.dy().dy()))
        elif i == Operation.Dz + 7:
          tree = tree_adder((val * item.dz().dz()))
        elif i == Operation.Dt + 7:
          tree = tree_adder((val * item.dt().dt()))
  return tree

def simplify_tree(expr, dim):
  if dim != 1 and dim != 2:
    raise RuntimeError("dim must be 1 or 2")
  tup = simplify_expression(expr)
  return to_tree(tup, dim)