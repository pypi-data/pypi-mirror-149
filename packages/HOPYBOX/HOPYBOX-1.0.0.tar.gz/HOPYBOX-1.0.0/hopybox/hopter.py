def Error_pta(error,pattern,text,value):
  print("\033[31m× {} in {} '{}':\n╰─ {}  ".format(error,pattern,value,text))
def Error_ptb(answer):
  print('\033[33mYour response (\'{}\') was not one of the expected responses: y, n Proceed (Y/n)?'.format(answer))