import os
from .hopt import Error_pta
from requests import get
def systems(order):
  print('\033[36m',end='\r')
  os.system(order)
def runpy(module):
  print('\033[0m',end='\r')
  os.system('python '+module)
def python():
  os.system('python')
def install(modules):
  print('\033[36m',end='\r')
  os.system('python3 -m pip install -U {}'.format(modules))
def uninstall(modules):
  print('\033[36m',end='\r')
  os.system('python3 -m pip uninstall {}'.format(modules))
def all_help():
  print('\033[36m'+str(get('https://hostudio123.github.io/HOPYBOX/help').text))
def module_help(module):
  print('\033[36m',end='\r')
  print(help(module))
def debug(command):
  try:
    print(eval(command))
  except Exception as e:
    print(e)