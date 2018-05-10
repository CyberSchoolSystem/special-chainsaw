from json import dumps, loads
import os
import sys

ip = sys.argv[1]
grade = '{"grade":"testKlasse6"}'
gcmd = "curl -X POST --data '" + grade + "' " + ip + ":3000/api/user/grade/add"
# print(gcmd)
gradeId = loads(os.popen(gcmd).read())['gradeId']

for i in range(1, 301):
    user = "helfer." + str(i)
    pw = "pw." + str(i)
    # print(user + "," + pw)

    data = {'firstName': user,
            'lastName': user,
            'gradeId': gradeId,
            'username': user,
            'password': pw,
            'role': {'citizen': True,
                     'representative': False,
                     'tech': False,
                     'admin': False,
                     'teacher': None,
                     'customs': False}}
    json = dumps(data)
    cmd = "curl -X POST --data '" + json + "' " + ip + ":3000/api/user/add"
    # print(cmd)
    os.system(cmd)

