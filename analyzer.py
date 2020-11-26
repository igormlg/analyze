#!/usr/bin/python3

import os
import sys
import requests

from dotenv import load_dotenv 

env_path = './.env'
load_dotenv(dotenv_path=env_path)

try:
  tail = os.getenv('TAIL')
  log = os.getenv('LOG')
  need_to_alert = int(os.getenv('NEEDTOALERT'))
  token = os.getenv('API_KEY')
  channel = os.getenv('CHANNEL_ID')
except:
  sys.exit(f'required env parameters are missing: TAIL or LOG or NEEDTOALERT or API_KEY or CHANNEL_ID')
  

temp = './temporary.log'
api_url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={channel}'


os.system(f'tail -{tail} {log} > {temp}')

f = open(temp, 'r')
requests_list = f.readlines()
f.close()
os.remove(temp)
ips_array = []


def find_in_array(ip, body):
  finded = False
  for x in ips_array:
    if x['ip'] == ip:
      x['count'] = x['count']+1
      finded = True
  if not finded:
    ips_array.append({'ip': ip, 'count': 1, 'body': body})

for req in requests_list:
  ip = req.split(' ')[0]
  body = req.split('"')[1]
  find_in_array(ip, body)
  

for reqs in ips_array:
  if reqs['count'] >= need_to_alert:
    message = 'С ip {} было сделано {} запросов. Последний {}'.format(reqs['ip'], reqs['count'], reqs['body'])
    requests.get(f'{api_url}&text={message}')