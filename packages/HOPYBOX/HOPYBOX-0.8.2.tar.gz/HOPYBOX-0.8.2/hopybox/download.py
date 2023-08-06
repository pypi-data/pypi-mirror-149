import os
import ssl
import wget
import time
import requests as visit
from .headers import headers_water
from .hopt import Error_pta
headers = headers_water()
ssl._create_default_https_context = ssl._create_unverified_context
def download(url):
  print('\033[32m',end='\r')
  try:
    res = visit.get(url,headers,stream=True)
  except Exception:
    Error_pta('DownloadError','Command','There was an error in the file download, please check whether the URL entered is correct','download …')
  else:
    try:
      file_size = int(res.headers['content-length'])
      print('File-Size:'+str(file_size)+'B')
      start_time = time.time()
      wget.download(url,'')
      end_time = time.time()
      spend_time = end_time-start_time
      print('',end='\n')
      print('Spend-Time:'+str(spend_time))
      print('Tips:Successfully downloaded this file')
    except Exception:
      Error_pta('DownloadError','Command','There was an error downloading the file, please check the connected network or URL for errors','download …')
      