from rich import console,syntax
def file_open(file):
  Console = console.Console()
  file = open(file,'rb')
  code = file.read().decode('utf-8')
  file.close()
  Console.print('\033[1m',end='\r')
  Console.print(syntax.Syntax(code,'python',theme="ansi_dark", line_numbers=True))