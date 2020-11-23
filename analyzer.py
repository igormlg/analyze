#!/usr/bin/python3

import os
import sys

try:
  tail = os.environ['TAIL']
  log = os.environ['LOG']
  need_to_alert = int(os.environ['NEEDTOALERT'])
except:
  sys.exit(f'required env parameters are missing: TAIL or LOG or NEEDTOALERT')
  

temp = './temporary.log'

os.system(f'tail -{tail} {log} > {temp}')

f = open(temp, 'r')
requests = f.readlines()
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

for req in requests:
  ip = req.split(' ')[0]
  body = req.split('"')[1]
  find_in_array(ip, body)
  

for reqs in ips_array:
  if reqs['count'] >= need_to_alert:
    print('С ip {} было сделано {} запросов. Последний {}'.format(reqs['ip'], reqs['count'], reqs['body']))