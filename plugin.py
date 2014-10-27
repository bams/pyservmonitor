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
    return '(name: \"%s\", menu: \"%s\", cmd: \"%s\")' % \
      (self.name, self.menu_txt, self.cmd)

'''
a tree that contains all commands/plugins
'''
class MyTree:

  def __init__(self, name='', data=None, depth=0):
    self.name = name
    self.data = data
    self.children = []
    self.depth = depth
    self._title = (data == None)

  def rec_get_name(self, cname):
    if self.name == cname and self.is_title():
      return self
    for c in self.children:
      ret = c.rec_get_name(cname)
      if ret != None:
        return ret
    return None

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

