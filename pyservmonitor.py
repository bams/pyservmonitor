#!/usr/bin/python
# server manager frontend
# author: deadc0de
#
# deps:
#   urwid (python-urwid in debian)

from plugin import *
from cfg_reader import cfg_reader
import argparse
from ui2 import *
import os
import sys

def err(string):
  sys.stderr.write(string+'\n')

def out(string):
  sys.stdout.write(string+'\n')

parser = argparse.ArgumentParser(description='server manager frontend')
parser.add_argument('--config', required=False,
  default='config.ini', help='the config file')
args = parser.parse_args()
cfg = args.config

# check user is root
#if os.geteuid() != 0:
#  err('get r00t !')
#  sys.exit(0)

if not os.path.isfile(cfg) or not os.path.exists(cfg):
  err('config file \"%s\" does not exist !' % (cfg))
  sys.exit(1)

cfgr = cfg_reader(cfg)
plugins = cfgr.get_plugins()
err('> %i entries parsed from config \"%s\"' % (len(plugins), cfg))

thetree = MyTree(name='commands')
for p in plugins:
  thetree.add(p.name, p)
ui(thetree)

