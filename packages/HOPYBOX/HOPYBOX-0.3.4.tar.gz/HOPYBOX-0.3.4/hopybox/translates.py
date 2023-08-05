import requests as visit
def translate(word):
  url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
  data={
'i':word,
'from':'AUTO',
'to':'AUTO',
'smartresult': 'dict',
'client': 'fanyideskweb',
'doctype': 'json',
'version': '2.1',
'keyfrom': 'fanyi.web',
'action': 'FY_BY_REALTIME',
'typoResult': 'false'
}
  res = visit.post(url,data=data)
  answer = res.json()
  result = answer["translateResult"][0][0]["tgt"]
  print('\033[32;1m{}'.format(result))