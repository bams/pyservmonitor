# the config file reader
# author: deadc0de
# format:
#   <name>:<menu-entry>:<command>

import re
import csv
from plugin import plugin

class cfg_reader():
  _path = None
  _plugins = []
  _DEBUG = False

  def __init__(self, path):
    self._path = path
    self._parse()

  def _parse(self):
    with open(self._path, 'r') as f:
      reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_MINIMAL, quotechar='\'', escapechar='\\')
      for row in reader:
        self._parse_line(row)

  def _parse_line(self, fields):
    if self._DEBUG:
      print 'parsing %s ...' % (fields)
    if len(fields) != 3:
      if self._DEBUG:
        print 'line %s too few elemtns' % (fields)
      return
    if fields[0][0] == '#':
      if self._DEBUG:
        print 'line %s is a comment' % (fields)
      return

    name = fields[0]
    entry = fields[1]
    cmd = fields[2]

    if self._DEBUG:
      print 'adding: %s' % (fields)
    self._plugins.append(plugin(name, entry, cmd))

  def get_plugins(self):
    return self._plugins
    
