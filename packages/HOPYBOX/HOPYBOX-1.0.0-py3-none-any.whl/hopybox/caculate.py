import math
import cmath
def caculate(num):
  if '+' in num or '-' in num or '*' in num or '/' in num or '%' in num and '√' not in num:
    try:
      num_run = eval(num)
      print('\033[32m'+num+'='+str(num_run))
    except SyntaxError as num_run:
      print('\033[31mSyntaxError:'+str(e))
    except ZeroDivisionError as e:
      print('\033[31mZeroDivisonError'+str(e))
  elif '√' in num and '*√' not in num:
    num_sqrt = math.sqrt(float(num))
    print('\033[32m√{0}={1:0.3}'.format(num,num_sqrt))
  elif '*√' in num:
     num_sqrt = cmath.sqrt(float(num))
     print('\033[32m√{0}={1:0.3f}j'.format(num,num_sqrt.imag))

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
  