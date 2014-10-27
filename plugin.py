# represent a plugin 
# author: deadc0de
#   - name
#   - menu entry
#   - cmd to execute

class plugin():
  ''' 
  @name: the plugin name
  @menu_txt: what will be displayed in the menu
  @cmd: command (shell one-liner) exected when menu selected
  '''
  def __init__(self, name, menu_txt, cmd):
    self.name = name
    self.menu_txt = menu_txt
    self.cmd = cmd

  def __repr__(self):
    return 'plugin object (name: \"%s\", menu: \"%s\", cmd: \"%s\")' % (self.name, self.menu_txt, self.cmd)

class MyTree:
  def __init__(self, name='', data=None, depth=0):
    self.name = name
    self.data = data
    self.children = []
    self.depth = depth
    self._title = False
    if data == None:
      self._title = True

  def rec_get_name(self, cname):
    if self.name == cname and self.is_title():
      return self
    if len(self.children) < 1:
      return None
    for c in self.children:
      return c.rec_get_name(cname)

  def is_title(self):
    return self._title
  
  def add(self, name, data):
    child = self.rec_get_name(name)
    if child == None:
      node = MyTree(name, data=None, depth=self.depth+1)
      node.children.append(MyTree(name, data, depth=self.depth+2))
      self.children.append(node)
    else:
      node = MyTree(name, data, depth=child.depth+1)
      child.children.append(node)

  def _print_node(self, indent):
    res = '\t'*indent
    res += 'name: %s (title: %s)\n' % (self.name, self._title)
    if not self.is_title():
      res += '\t'*indent + 'data: '
      res += str(self.data)
    return res + '\n'

  def print_tree(self, indent=0):
    res = self._print_node(indent)
    for c in self.children:
      res += c.print_tree(indent+1)
    return res
  
  def __repr__(self):
    return self.print_tree()

