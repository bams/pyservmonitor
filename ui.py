# the gui
# author: deadc0de
#

import urwid # python-urwid
import subprocess
import getpass
import datetime
import sys

class Entry(urwid.Text):
  def selectable(self):
      return True
  def keypress(self,  size,  key):
      return key

# each tree has nodes. Each node 
# contains a widget that's used
# for displaying the content of the entry.
# The ParentNode's task is to maintain
# order in the nodes in the tree

def err(string):
  sys.stderr.write('%s\n' % (string))

# the different widgets in the tree view
class TextTreeWidget(urwid.TreeWidget):
  # is called by parent node
  # to get the content
  # get_node().get_value() returns the tuple
  def get_display_text(self):
    err('get_display_text')
    err(str(self.get_node().get_value()))
    err(type(self.get_node().get_value()))
    err(len(self.get_node().get_value()))

    v = self.get_node().get_value()
    if type(v) == dict:
      err('item: ' + v.items()[0][0])
      return v.items()[0][0]
    else:
      return v[0]

class CmdTreeWidget(urwid.TreeWidget):
  def get_display_text(self):
    return 'a cmd widget'

class EmptyTreeWidget(urwid.TreeWidget):
  def get_display_text(self):
    return 'an empty widget'

# the different nodes in the tree view
class TextNode(urwid.TreeNode):
  def load_widget(self):
    return TextTreeWidget(self)

class CmdNode(urwid.TreeNode):
  def load_widget(self):
    return CmdTreeWidget(self)

class EmptyNode(urwid.TreeNode):
  def load_widget(self):
    return EmptyTreeWidget(self)

# the parent node
class EntryNode(urwid.ParentNode):

  def load_widget(self):
    return TextTreeWidget(self)

  def load_child_keys(self):
    err('load_child_keys: ')
    err(self.get_value())
    err('keys:')
    err(range(len(self.get_value().items())))
    return range(len(self.get_value().items()))

  def load_child_node(self, key):
    err('load_child_node: ')
    err(self.get_value())
    err('key: %i' % (key))
    if key == None:
      # child
      return EmptyNode(None)
    else:
      # parent
      err('load_child_node2:')
      err(str(self.get_value().items()[key]))
      return TextNode(self.get_value().items()[key])

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

  header_txt = 'Server monitor 0.2 (user: \'%s\') - by https://deadc0de6.github.io' % (getpass.getuser())
  footer_txt = ' | cmd: '
  empty_txt = [
    Entry('Please select an element above:'),
    Entry('   Enter:   select'),
    Entry('   r:       reload'),
    Entry('   up/down: navigate'),
    Entry('   j/k:     navigate'),
    Entry('   h:       display this help'),
    Entry('   q:       quit'),
    Entry('   +:       expand'),
    Entry('   -:       fold'),
  ]

  def __init__(self, up_entries, script_match):
    self.up_entries = up_entries
    self.script_match = script_match

    # the north panel
    self.northPanel = urwid.TreeListBox(urwid.TreeWalker(EntryNode(up_entries)))

    # the south panel
    self.content = urwid.SimpleListWalker(self.get_south_content(''))
    self.southPanel = urwid.ListBox(self.content)

    # the global content
    # LineBox add a surrounding box around the widget
    self.cont = urwid.Pile([('fixed', 10, urwid.LineBox(self.northPanel)), urwid.LineBox(self.southPanel),])
    # create the header
    header = urwid.AttrMap(urwid.Text(self.header_txt), 'head')
    footer = urwid.AttrMap(urwid.Text(self.get_date() + self.footer_txt), 'head')
    # create the global frame
    self.view = urwid.Frame(self.cont, header=header, footer=footer)
    # start the main loop
    loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.keystroke, handle_mouse=False)
    loop.run()

  def get_date(self):
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  def extexec(self, cmd):
    text = []
    if cmd == None or cmd == '':
      return ('', False)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
      if line == None:
        continue
      text.append(line.rstrip())
    ret = p.wait()
    return (text, ret)

  def get_south_content(self, cmd):
    if cmd == '':
      content = [urwid.AttrWrap(w, None, 'south') for w in self.empty_txt]
    else:
      (text, ret) = self.extexec(cmd)
      if text == '' or ret != 0:
        content = [urwid.AttrMap(w, None, 'south') for w in self.empty_txt]
      else:
        content = [urwid.AttrMap(Entry(w), None, 'south') for w in text]
    return content

  def set_header(self, txt):
    # update header
    self.view.set_header(urwid.AttrWrap(urwid.Text(
        self.header_txt + txt), 'head'))

  def set_footer(self, txt):
    # update footer
    self.view.set_footer(urwid.AttrWrap(urwid.Text(
        self.get_date() + self.footer_txt + txt), 'head'))

  def update_display(self):
    focus, pos = self.northPanel.get_focus()
    cmd = self.script_match.get(pos)
    if cmd == '':
      return
    # TODO
    #self.set_header(' - item %s' % (str(self.up_entries[pos].get_text()[0])))
    self.set_footer('\"%s\"' % (cmd))
    # update south pane
    self.content[:] = self.get_south_content(cmd)

  # return True if focus is on north widget
  def get_focus_up(self):
    l = self.cont.widget_list
    idx = l.index(self.cont.focus_item)
    return idx == 0

  def set_focus(self, up):
    l = self.cont.widget_list
    if up:
      self.cont.set_focus(l[0])
    else:
      self.cont.set_focus(l[1])

  def inv_focus(self):
    up = self.get_focus_up()
    if up:
      set_focus(False)
    else:
      set_focus(True)

  def keystroke(self, input):
      if input in ('q', 'Q'):
          raise urwid.ExitMainLoop()

      if input is 'enter' or input is ' ':
        self.update_display()

      if input is 'r':
        self.update_display()

      if input is 'j':
        if self.get_focus_up():
          focus, pos = self.northPanel.get_focus()
          if pos >= len(self.north_entries)-1:
            return
          self.northPanel.set_focus(pos+1)
        else:
          focus, pos = self.southPanel.get_focus()
          if pos >= len(content)-1:
            return
          self.southPanel.set_focus(pos+1)

      if input is 'k':
        if self.get_focus_up():
          focus, pos = self.northPanel.get_focus()
          if pos == 0:
            return
          self.northPanel.set_focus(pos-1)
        else:
          focus, pos = self.southPanel.get_focus()
          if pos == 0:
            return
          self.southPanel.set_focus(pos-1)

      if input is 'h' or input is '?': # help
        self.content[:] = self.get_south_content('')

      if input is 'tab':
        inv_focus()

