import os
import requests as visit
from .hopter import Error_pta
from .headers import headers_water
headers = headers_water()
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
  try:
    print('\033[36m'+str(visit.get('https://hostudio123.github.io/HOPYBOX/help',headers=headers).text))
  except:
    Error_pta('GetHelpError','Command','Unable to get help documentation','help')
def license():
  try:
    print('\033[36m'+str(visit.get('https://hostudio123.github.io/LICENSE',headers=headers).text))
  except:
    Error_pta('GetLicenseError','Command','Unable to get license documentation','license')
def module_help(module):
  print('\033[36m',end='\r')
  print(help(module))
def debug(command):
  try:
    print(eval(command))
  except Exception as e:
    print(e)