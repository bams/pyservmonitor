
import npyscreen
import curses

class NorthBox(npyscreen.BoxBasic):
  _contained_widget = npyscreen.MLTreeMultiSelect

class SouthBox(npyscreen.BoxBasic):
  _contained_widget = npyscreen.TitleText,

class TreeWidget(npyscreen.MLTree):
  def when_cursor_moved(self):
    print 'moved'
    print self.value
    #print self.super.super.get_selected_objects()
    print self.value
  def when_value_edited(self):
    #print 'edited !!!!!!!!!!!!!!!!!!!'
    pass

class tui(npyscreen.NPSApp):

  def add_tree(self, tree):
    self.tree = tree 

  def add_handlers(self, handlers):
    self.handlers = handlers

  def main(self):
    form = npyscreen.Form(name='title')
    box = form.add(TreeWidget, name='Output',
      values=self.tree, value=self.tree, max_height=10)
    box.add_handlers(self.handlers)
    self.north = box
    form.add(SouthBox, name='Commands', value='output stuff')
    form.edit()

class ui():
  def h_right(self, *args, **keywords):
    print 'h_right called'
    print args
    #print keywords
    #print self.ta.north
    #print self.ta.north.get_selected_objects()

  def def_handlers(self):
    self.handlers = {
        curses.KEY_RIGHT:  self.h_right,
      }
  
  def __init__(self, tree):

    self.def_handlers()
    treedata = npyscreen.TreeData(content='Root',
      selectable=False, ignore_root=False)
    for c in tree.children:
      self.add_sub_tree(c, treedata)

    self.ta = tui()
    self.ta.add_tree(treedata)
    self.ta.add_handlers(self.handlers)
    self.ta.run()

  def add_sub_tree(self, node, root):
    for c in node.children:
      if c.is_title():
        cont = '%s' % (c.name)
      else:
        cont = '%s - %s' % (c.name, c.data.menu_txt)
      child = root.new_child(content=cont, selectable=False)
      #child.add_handlers(self.handlers)
      self.add_sub_tree(c, child)

  def key_handler(self):
    print 'handler called'

