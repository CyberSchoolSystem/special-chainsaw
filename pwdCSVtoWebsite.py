#!/usr/local/bin/python
import csv
import requests
import json

def toDict(d):
    n = {}
    for i in d:
        n[i['name']] = i['id']
    return n

login_url = 'http://localhost:3000/auth/page/hashdb/login'
payload = {'username': "jesus", 'password': "123"}
session = requests.Session()
req = session.post(login_url, data=payload, verify=False)
grades = toDict(session.get('http://localhost:3000/api/user/grade/info').json())
print(req)

with open('passwords.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    lines = sum(1 for row in readCSV)

with open('passwords.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    current = 1
    for row in readCSV:
        klasse = row[0]
        if klasse == "":
            klasse = "Lehrer"
        name = row[1]
        username = row[2]
        password = row[3]
        vorname = name.split(" ")[0]
        nachname = name.split(" ")[1]
        print(str(current) + "/" + str(lines) + ": " + username)
        current +=1
        data = {'firstName': vorname,
                'lastName': nachname,
                'gradeId': grades[klasse],
                'username': username,
                'password': password,
                'role': {'citizen': True,
                        'representative': False,
                        'tech': False,
                        'admin': False,
                        'teacher': None,
                        'customs': False
                        }
                }
        q = session.post("http://localhost:3000/api/user/add", data=json.dumps(data), verify=False)
        print (q)
