import requests as visit
from bs4 import BeautifulSoup as bs
from .translates import translate as tran
#IP
def _get_ip(ip,headers):
  global res
  try:
    res = visit.get('https://q.ip5.me/?s='+ip,headers=headers)
  except Exception:
    print('\033[31;1mHOPYBOX:FIND:IPV4:NotFindIPError:The address of this IP address was not found')
#IPV4way
def ipv4way(ip,headers):
  _get_ip(ip,headers)
  soup = bs(res.text, 'html.parser')
  items = soup.find_all('div',style='color:#FF0000; word-break:break-all;')
  try:
    way_js = str(items).split('>')
    ipv4way = str(str(way_js[1].split()).split('<')[0]).split('[\'')
    if '\', \'' in ipv4way[1]:
      ipway = str(ipv4way[1]).split('\', \'')
      print('\033[32;1mHOPYBOX:IPV4WAY:{}'.format(ipway[0]+ipway[1]))
    elif ipv4way[1] == 'IP地址不合法，仅支持IPv4地址，且每次只能查询一个，请重新输入。':
      print('\033[31;1mHOPYBOX:FIND:IPV4:NotFindIPError:The address of this IP address was not found')
    elif ipv4way[1] == '局域网对方和您在同一内部网':
      print('\033[31;1mHOPYBOX:IPLANError:The other side of the LAN is on the same intranet as you')
    else:
      print('\033[32;1mHOPYBOX:IPV4WAY:{}'.format((ipv4way[1])))
  except Exception:
    print('\033[31;1mHOPYBOX:FIND:IPV4:NotFindIPError:The address of this IP address was not found')
#IP Whole
def ip_wholeway(ip,headers):
 # http://mip.chinaz.com/?query=
  pass