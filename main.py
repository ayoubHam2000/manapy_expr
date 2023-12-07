import re
from collections import deque

class Tree:
  def __init__(self):
    self.token = ""
    self.left = None
    self.right = None

  def __parse(self, query : str, node):
    operator = re.search(r'=', query)
    if operator:
      s1 = query[0: operator.start()]
      s2 = query[operator.start() + 1:]
      node.token = operator.group(0).strip()
      node.left = self.__parse(s1, Tree())
      node.right = self.__parse(s2, Tree())
      return node
    operator = re.search(r'\+|-', query)
    if operator:
      s1 = query[0: operator.start()]
      s2 = query[operator.start() + 1:]
      node.token = operator.group(0).strip()
      node.left = self.__parse(s1, Tree())
      node.right = self.__parse(s2, Tree())
      return node
    operator = re.search(r'\*|\.', query)
    if operator:
      s1 = query[0: operator.start()]
      s2 = query[operator.start() + 1:]
      node.token = operator.group(0).strip()
      node.left = self.__parse(s1, Tree())
      node.right = self.__parse(s2, Tree())
      return node
    node.token = query.strip()
    return node
  
  def parse(self, query : str):
    self.__parse(query, self)
  
  ##########################################
  ## Replacer
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
          self.__print_item_in_center(node.token, buffer_size)
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

  def print(self):
    h = self.tree_height(self) + 1
    self.__print_tree(h)

tree = Tree()
tree.parse("A + d.dB = 10")
tree.print()