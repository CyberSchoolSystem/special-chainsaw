from escpos.printer import Usb
import requests, json
import random, string
import sys

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def hasUser(d, u):
    for i in d:
        if u == i['username']:
            return True
    return False


def printInfo(user, password):
	p.set(font='a', height=2, width=2, align='center')
	p.text("Dein neues\n")
	p.text("Passwort:\n")
	p.set(font='a', height=1, width=1, align='left', text_type='B')
	p.text("Benutzername:\n")
	p.set(font='a', height=1, width=1, align='left', text_type='NORMAL')
	p.text(user)
	p.text("\n\n")
	p.set(font='a', height=1, width=1, align='left', text_type='B')
	p.text("Passwort:\n")
	p.set(font='a', height=1, width=1, align='left', text_type='NORMAL')
	p.text(password)
	p.text("\n\n\n\n")


login_url = 'http://' + sys.argv[1] + '/auth/page/hashdb/login'
payload = {'username': sys.argv[2], 'password': sys.argv[3]}
session = requests.Session()
req = session.post(login_url, data=payload, verify=False)
users = session.post('http://' + sys.argv[1] + '/api/user/info', json={}).json()

#print(json.dumps(users, indent=4))

p = Usb(0x0456, 0x0808, 4, 0x81, 0x03)
p.charcode("MULTILINGUAL")

username = sys.argv[4]
password = randomword(6)

if hasUser(users, username):
	print("Updating user: " + username)
	data = {'idUsername': username, 'password': password }
	q = session.post("http://" + sys.argv[1] + '/api/user/update', json=data).text
	print(q)
	printInfo(username, password)

else:
	print("Der Benutzer " + username + " existiert nicht!")


