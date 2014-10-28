# the gui
# author: deadc0de
#

import urwid # python-urwid
import subprocess
import getpass
import datetime
import sys
from plugin import *

# TODO
# - add color border when focus up or down
# - add color focus on selected item
# - auto-select child when parent is selected
# - remove tree root

'''
Doc is definitely not helpful
  each tree has nodes. Each node 
  contains a widget that's used
  for displaying the content of the entry.
  The ParentNode's task is to maintain
  order in the nodes in the tree
'''

'''
These functions help for debug
as nothing gets printed on 
console ;-)
'''
def err(string):
  sys.stderr.write('%s\n' % (string))

def errlog(string):
  f = open('/tmp/x', 'a')
  f.write(str(string) + '\n')
  f.close()

'''
this is a normal entry
in the south panel
'''
class Entry(urwid.Text):

  def selectable(self):
      return True

  def keypress(self,  size,  key):
      return key

'''
by using our own subclass of urwid.Pile
we are able to handle the macro keys
and complete it with our owns
'''
class MyPile(urwid.Pile):
  def keypress(self, size, key):
    if key == 'j':
      key = 'down' 
    elif key == 'k':
      key = 'up'
    nkey = self.__super.keypress(size, key)
    return nkey

'''
the different widgets in the tree view
can be either a title or a command that
will be executed and its result displayed
in the south panel
'''
class TextTreeWidget(urwid.TreeWidget):

  def __init__(self, node):
    self.__super.__init__(node)
    self.expanded = True
    self.update_expanded_icon()

  #def unfold(self, val):
  #  self.expanded = val
  #  self.update_expanded_icon()

  def selectable(self):
    return True
  
  # capture the key before parent
  def keypress(self, size, key):
    elem = self.get_node().get_value()
    skey = key
    key = self.__super.keypress(size, key)
    if skey == 'right' or key == ' ' or key == 'enter':
      return 'enter'
    return key

  # is called by parent node
  # to get the content
  def get_display_text(self):
    elem = self.get_node().get_value()
    if elem.is_title():
      return elem.name
    else:
      return elem.data.menu_txt

'''
the text node wrapping the text widget
'''
#class TextNode(urwid.TreeNode):
#
#  def load_widget(self):
#    return TextTreeWidget(self)

'''
a node with children
'''
class EntryNode(urwid.ParentNode):

  def load_widget(self):
    widget = TextTreeWidget(self)
    return widget

  def load_child_keys(self):
    return range(len(self.get_value().children))

  def load_child_node(self, key):
    elem = self.get_value()
    nchild = elem.children[key]
    ndepth = elem.depth + 1
    if elem.is_title():
      return EntryNode(nchild, parent=self, key=key, depth=ndepth)
    return None
    #else:
    #  return TextNode(nchild, parent=self, key=key, depth=ndepth)

'''
the ui class
'''
class ui():

  # this defines the color for the different elements
  # format: <keyword>, <font color>, <background color> <display attr>
  palette = [
      ('body','dark cyan', '', 'standout'),
      ('focus','dark red', '', 'standout'),
      ('head','light red', 'black'),
      ('north', 'dark cyan', '', 'standout'),
      ('south', 'yellow', ''),
      ]

  header_txt = 'Server monitor 0.3 (user: \'%s\') - by https://deadc0de6.github.io' % (getpass.getuser())
  footer_txt = ' | cmd: '
  empty_txt = [
    Entry('Please select an element above:'),
    Entry('   Enter:   select'),
    Entry('   up/down: navigate'),
    Entry('   j/k:     navigate'),
    Entry('   h/?:     display this help'),
    Entry('   q:       quit'),
    Entry('   tab:     change focus up/down'),
    Entry('   +:       expand'),
    Entry('   -:       fold'),
    Entry('   right:   open children'),
    Entry('   left:    get parent'),
  ]

  def __init__(self, entries):
    self.entries = entries

    # the north panel
    node = EntryNode(entries)
    self.northPanel = urwid.TreeListBox(urwid.TreeWalker(node))

    # the south panel
    self.content = urwid.SimpleListWalker(self.get_south_content(''))
    self.southPanel = urwid.ListBox(self.content)

    # the global content
    # LineBox adds a surrounding box around the widget
    self.cont = MyPile([('fixed', 10, urwid.LineBox(self.northPanel)),
      urwid.LineBox(self.southPanel),])
    # create the headers
    header = urwid.AttrMap(urwid.Text(self.header_txt), 'head')
    footer = urwid.AttrMap(urwid.Text(self.get_date() +
      self.footer_txt), 'head')
    # create the global frame
    self.view = urwid.Frame(self.cont, header=header, footer=footer)
    # start the main loop
    loop = urwid.MainLoop(self.view, self.palette,
      unhandled_input=self.keystroke, handle_mouse=False)
    loop.run()

  def get_date(self):
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # execute external command
  def extexec(self, cmd):
    text = []
    if cmd == None or cmd == '':
      return ('', False)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
      if line == None:
        continue
      text.append(line.rstrip())
    ret = p.wait()
    return (text, ret)

  # this returns the content of the south panel
  def get_south_content(self, cmd):
    if cmd == '':
      '''
      here we handle the text in the south panel
      the AttrWrap allows to set its attribute (focus, ...)
      '''
      content = [urwid.AttrWrap(w, None) for w in self.empty_txt]
    else:
      '''
      here we fill the south panel
      with command outputs
      '''
      (text, ret) = self.extexec(cmd)
      if text == '' or ret != 0:
        content = [urwid.AttrMap(Entry('<no output>'), None)]
        #content = [urwid.AttrMap(w, None) for w in self.empty_txt]
      else:
        content = [urwid.AttrMap(Entry(w), None, focus_map='south') for w in text]
    return content

  # update header
  def set_header(self, txt):
    self.view.set_header(urwid.AttrWrap(urwid.Text(
        self.header_txt + txt), 'head'))

  # update footer
  def set_footer(self, txt):
    self.view.set_footer(urwid.AttrWrap(urwid.Text(
        self.get_date() + self.footer_txt + txt), 'head'))

  # this gets called when an entry is selected
  # in the north panel
  def update_display(self):
    widget, node = self.northPanel.get_focus()
    elem = widget.get_node().get_value()
    if not elem.is_title():
      cmd = elem.data.cmd
      name = elem.data.name
      self.set_footer('\"%s\"' % (cmd))
      self.set_header(' - item %s' % (name))
      self.content[:] = self.get_south_content(cmd)
    else:
      self.set_footer('')

  # return True if focus is on north widget
  def get_focus_up(self):
    l = self.cont.widget_list
    idx = l.index(self.cont.focus_item)
    return idx == 0

  def set_focus(self, up):
    l = self.cont.widget_list
    if up:
      self.cont.set_focus(l[0]) # north panel
    else:
      self.cont.set_focus(l[1]) # south panel

  def inv_focus(self):
    up = self.get_focus_up()
    if up:
      self.set_focus(False)
    else:
      self.set_focus(True)

  def keystroke(self, input):
      self.set_footer('\"%s\"' % (input))
      if input in ('q', 'Q'):
          raise urwid.ExitMainLoop()
      elif input is 'enter' or input is ' ' or input is 'right':
        self.update_display()
        #self.northPanel.focus_home((10, 10))
      elif input is 'r':
        self.update_display()
      elif input is 'h' or input is '?': # help
        self.content[:] = self.get_south_content('')
      elif input is 'tab':
        self.inv_focus()

