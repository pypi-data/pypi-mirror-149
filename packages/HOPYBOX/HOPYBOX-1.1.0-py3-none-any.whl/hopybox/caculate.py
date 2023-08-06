import math
import cmath
from .hopter import Error_pta
def caculate(num):
  num_logos = ['+','-','*','/','%','|','&','^','~','>>','<<']
  for i in num_logos:
    if i in num:
      try:
        print('\033[92m'+str(eval(num)))
      except SyntaxError as e:
        Error_pta('SyntaxError','Command',str(e),num)
      except ZeroDivisionError as e:
        Error_pta('ZeroDivisonError','Command',str(e),num)
    else:
      pass
    break
def root_caculate(num):
  if '√' in float(num):
    if num >= 0:
      print('\033[92m'+str(math.sqrt(float(num))))












#def caculates(num):
       #and 
    
  #elif '√' in num and '*√' not in num:
    #num_sqrt = math.sqrt(float(num))
    #print('\033[32m√{0}={1:0.3}'.format(num,num_sqrt))
  #elif '*√' in num:
     #num_sqrt = cmath.sqrt(float(num))
     #print('\033[32m√{0}={1:0.3f}j'.format(num,num_sqrt.imag))

def nmaths(num):
  num_sqrt = math.sqrt(float(num))
  print('\033[32;1mHOPYBOX:MATH:±√{0}=±{1:0.3}'.format(num,num_sqrt))
def smath(num,run):
  print('\033[32;1mHOPYBOX:MATH:',end='')
  if run == 1:
    print(math.sin(math.radians(num)))
  if run == 2:
    print(math.cos(math.radians(num)))
  if run == 3:
    print(math.tan(math.radians(num)))
  if run == 4:
    print(math.asin(num))
  if run == 5:
    print(math.acos(num))
  if run == 6:
    print(math.atan(num))
def symbol(text):
  symbol = ['√','sin','cos','tan','asin','acos','atan']
  for i in range(len(symbol)):
    if symbol[i] in text:
      del symbol
      i = 'have'
      break
      return False
  if i != 'have':
      return True
  