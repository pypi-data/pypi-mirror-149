import os
import filetype
import zipfile,tarfile
import time
from rich import console,syntax
from .hopter import Error_pta,Error_ptb
def open_file(filename):
  print('File-Size:{}B'.format(os.stat(filename).st_size))
  print('File-Dev:{}'.format(os.stat(filename).st_dev))
  print('Fie-Nlink:{}'.format(os.stat(filename).st_nlink))
  print('File-Ino:{}'.format(os.stat(filename).st_ino))
  mtime = time.localtime(os.stat(filename).st_mtime)
  mtime = time.strftime("%Y/%m/%d %H:%M:%S",mtime)
  print('File-Mtime:{}'.format(mtime))
  print('File-Content:\033[0m')
  print('Loaing …',end='\r')
  file_open(filename)
def read_file(filename):
  try:
    filekind = filetype.guess(filename)
    if filekind is None:
      print('\033[32mFile-Type:text')
      mode = 'r'
      open_file(filename)
    else:
      file_type = filekind.extension
      print('\033[32mFile-Type:%s' % file_type)
      if file_type == 'png' or file_type == 'jpg':
        mode = 'rb'
        openfile(filename)
      elif file_type == 'zip':
        zip = zipfile.ZipFile(filename)
        print(zip.filename)
        for i in range(len(zip.namelist())):
          print('|__'+zip.namelist()[i])
        while True:
          unfile_answer = input('\033[32mHOPYBOX:FILE:UNZIP:Do you want to unzip to the current directory?(Y/n)')
          if unfile_answer == 'Y' or unfile_answer == 'y':
            zip.extractall()
            print('\033[32mDecompression command executed')
            break
          elif unfile_answer == 'n':
            break
          else:
            Error_ptb(unfile_answer)
        else:
          pass
  except FileNotFoundError as e:
    print('\033[31mFileNotFoundError:{}'.format(e))
  except UnicodeDecodeError as e:
    print('\033[31mUnicodeDecodeError:{}'.format(e))
  except IsADirectoryError as e:
    print('\033[31mIsADirectoryError:{}'.format(e))
  except PermissionError as e:
    print('\033[31mHOPYBOX:FILE:PermissionError:{}'.format(e))

def file_open(filename):
  Console = console.Console()
  file = open(filename,'rb')
  code = file.read().decode('utf-8')
  file.close()
  extension = os.path.splitext(filename)[1]
  if extension == '.py':
    Console.print(syntax.Syntax(code,'python',theme="ansi_dark", line_numbers=True))
  elif extension == '.html':
    Console.print(syntax.Syntax(code,'html',theme="ansi_dark", line_numbers=True))
  elif extension == '.cpp' or extension == 'c':
    Console.print(syntax.Syntax(code,'c',theme="ansi_dark", line_numbers=True))
  elif extension == '.java':
    Console.print(syntax.Syntax(code,'java',theme="ansi_dark", line_numbers=True))
  else:
    Console.print(syntax.Syntax(code,'text',theme="ansi_dark", line_numbers=True))