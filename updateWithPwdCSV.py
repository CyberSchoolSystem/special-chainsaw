#!/usr/local/bin/python
import csv
import requests
import json
import sys
import random, string


def toDict(d):
    n = {}
    for i in d:
        n[i['name']] = i['id']
    return n

def hasUser(d, u):
    for i in d:
        if u == i['username']:
            return True
    return False

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def mkPasswd(r):
    t = open('new-pws.csv', 'a')
    pw = randomword(6)
    # Username, Last name, FirstName, pw, grade
    out = ';'.join([row[0], row[2], row[1], pw, row[4]]) + '\n'
    t.write(out)
    return pw


login_url = 'http://' + sys.argv[1] + '/auth/page/hashdb/login'
payload = {'username': sys.argv[2], 'password': sys.argv[3]}
session = requests.Session()
req = session.post(login_url, data=payload, verify=False)

grades = toDict(session.get('http://' + sys.argv[1] + '/api/user/grade/info').json())
users = session.post('http://' + sys.argv[1] + '/api/user/info', json={}).json()

currUsers = []
stage = int(sys.argv[4])
with open('new-list.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    if stage == 1:
        for row in readCSV:
            username = row[0].lower()
            if hasUser(users, username):
                print("Updating user: " + username)
                data = {'idUsername': username,
                        'password': mkPasswd(row),
                        'gradeId': grades[row[4]]}
                q = session.post("http://" + sys.argv[1] + '/api/user/update',
                                json=data).text
                print(q)
            else:
                data = {'firstName': row[1],
                        'lastName': row[2],
                        'gradeId': grades[row[4]],
                        'username': row[0],
                        'password': mkPasswd(row),
                        'role': {'citizen': True,
                                'representative': False,
                                'tech': False,
                                'admin': False,
                                'teacher': None,
                                'customs': False
                                }
                        }
                q = session.post('http://' + sys.argv[1] + '/api/user/add',
                                json=data).text
                print("Adding user: " + username)
                print(q)

    if stage == 2:
        for row in readCSV:
                currUsers.append(row[0].lower())
        for u in users:
            if u['username'] not in currUsers:
                print("Deleting user: " + u['username'])
                q = session.post('http://' + sys.argv[1] + '/api/user/remove',
                                json={'idUsername': u['username']}).text
                print(q)
