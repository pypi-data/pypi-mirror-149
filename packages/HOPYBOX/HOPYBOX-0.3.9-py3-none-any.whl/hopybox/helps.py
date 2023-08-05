def all_help():
  print('''\033[32mCommand (take command) 
1.Help
├ help 
└ help <module> 
2.Id
└ id <text> 
3.Runpy
└ run <file> 
4.Hoget
└ hoget <url> 
5.Browse
└ bowget <url> 
6.QQ
├ qqname <qqnumber> 
└ qqhead <qqnumber> 
7.Exit
└exit 
System (take system) 
└exit 
Python (take python) 
├ debug <command> 
└ interpreter 
Last
└ If you have any questions, please contact the developer as HOStudio.hopybox@foxmail.com ''')
def module_help(module):
  print('\033[32m',end='\r')
  print(help(module))