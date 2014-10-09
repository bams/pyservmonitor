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
    return 'name: \"%s\", menu: \"%s\", cmd: \"%s\"' % (self.name, self.menu_txt, self.cmd)
