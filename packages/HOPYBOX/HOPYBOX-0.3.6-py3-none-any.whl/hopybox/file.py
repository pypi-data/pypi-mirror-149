import os
import filetype
import zipfile
import time
mode = 'r'
def _openfile(filename):
  print('FILE:SIZE:{}B'.format(os.stat(filename).st_size))
  print('FILE:DEV:{}'.format(os.stat(filename).st_dev))
  print('HOPYBOX:FILE:NLINK:{}'.format(os.stat(filename).st_nlink))
  print('HOPYBOX:FILE:INO:{}'.format(os.stat(filename).st_ino))
  mtime = time.localtime(os.stat(filename).st_mtime)
  mtime = time.strftime("%Y/%m/%d %H:%M:%S",mtime)
  print('HOPYBOX:FILE:MTIME:{}'.format(mtime))
  print('HOPYBOX:FILE:CONTENT:\033[0m\033[1m')
  print('PIease wait …\033[0m',end='\r')
  file_open(filename)
  print('\033[32;1mHOPYBOX:FILE:CLOSE')
def read_file(filename):
  try:
    _filekind = filetype.guess(filename)
    if _filekind is None:
      print('\033[32;1mHOPYBOX:FILE:TYPE:TEXT')
      _mode = 'r'
      _openfile(filename)
    else:
      print('\033[32;1mHOPYBOX:FILE:TYPE: %s' % _filekind.extension)
      _filetype_ = _filekind.extension
      if _filetype_ == 'png':
        _mode = 'rb'
        _openfile(filename)
      if _filetype_ == 'jpg':
        _mode = 'rb'
        _openfile(filename)
      elif _filetype_ == 'zip':
        zip = zipfile.ZipFile(filename)
        print('HOPYBOX:FILE:ZIPCENTENT:'+zip.filename)
        for i in range(len(zip.namelist())):
          print('|__'+zip.namelist()[i])
        while True:
          howun = input('\033[32;1mHOPYBOX:FILE:UNZIP:Do you want to unzip to the current directory?(y/n)')
          if howun == 'y':
            zip.extractall()
            print('\033[32;1mHOPYBOX:FILE:UNZIP:Decompression command executed')
            break
          elif howun == 'n':
            break
          else:
            print('\033[32;1mHOPYBOX:FILE:UNZIP:Your response (\'{}\') was not one of the expected responses: y, n Proceed (y/n)?'.format(howun))
  except FileNotFoundError as log:
    print('\033[31;1mHOPYBOX:FILE:FileNotFoundError:{}'.format(log))
  except UnicodeDecodeError as log:
    print('\033[31;1mHOPYBOX:FILE:UnicodeDecodeError:{}'.format(log))
  except IsADirectoryError as log:
    print('\033[31;1mHOPYBOX:FILE:IsADirectoryError:{}'.format(log))
  except PermissionError as log:
    print('\033[31;1mHOPYBOX:FILE:PermissionError:{}'.format(log))
def refile(filename):
  try:
    os.remove(filename)
    print('\033[32;1mHOPYBOX:FILE:RF:FILE:{}'.format(filename))
  except FileNotFoundError as log:
    print('\033[31;1mHOPYBOX:FILE:FileNotFoundError:{}'.format(log))
  except IsADirectoryError as log:
    print('\033[31;1mHOPYBOX:FILE:IsADirectoryError:{}'.format(log))
  except PermissionError as log:
    print('\033[31;1mHOPYBOX:FILE:PermissionError:{}'.format(log))
   
def repath(pathname):
  try:
    os.rmdir(pathname)
    print('\033[32;1mHOPYBOX:FILE:RF:PATH:{}'.format(pathname))
  except FileNotFoundError as log:
    print('\033[31;1mHOPYBOX:FILE:FileNotFoundError:{}'.format(log))
  except IsADirectoryError as log:
    print('\033[31;1mHOPYBOX:FILE:IsADirectoryError:{}'.format(log))
  except PermissionError as log:
    print('\033[31;1mHOPYBOX:FILE:PermissionError:{}'.format(log))
  except OSError as log:
    print('\033[31;1mHOPYBOX:FILE:OSError:{}'.format(log))

from rich import console,syntax
def fileopen(file):
  Console = console.Console()
  file = open(file,'rb')
  code = file.read().decode('utf-8')
  file.close()
  Console.print('\033[1m',end='\r')
  Console.print(syntax.Syntax(code,'python',theme="ansi_dark", line_numbers=True))