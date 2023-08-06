def Error_pta(error,pattern,text,value):
  print("\033[91m× {} in {} '{}':\n╰─ {}  ".format(error,pattern,value,text))
def Error_ptb(answer):
  print('\033[93mYour response (\'{}\') was not one of the expected responses: y, n Proceed (Y/n)?'.format(answer))