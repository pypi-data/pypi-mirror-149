import os
import requests as visit
from bs4 import BeautifulSoup as bs
from .version import version_number as version
def check_version():
  global visit
  global version
  res = visit.get('https://hostudio123.github.io/HOPYBOX/version')
  print('Detecting in version …',end='\r')
  if version >= int(res.text):
    print("\033[36mResult:Your HOPYBOX is the latest version")
  else:
    print('\033[36mResult:New version found on the official website of HOPYBOX')
    os.system('python3 -m pip install -U HOPYBOX')