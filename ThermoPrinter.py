from escpos.printer import Usb
import requests, json
import random, string
import sys, os
import readline, glob

class tabCompleter(object):
    def createListCompleter(self,ll):
        def listCompleter(text,state):
            line = readline.get_line_buffer()

            if not line:
                return [c + " " for c in ll][state]

            else:
                return [c + " " for c in ll if c.startswith(line)][state]
    
        self.listCompleter = listCompleter

def randomword(length):
   letters = string.ascii_letters + string.digits + "!.-"
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

usernames = []

for i in users:
	if(i['username'] != ''):
		usernames.append(i['username'])

#print(json.dumps(users, indent=4))

p = Usb(0x0456, 0x0808, 4, 0x81, 0x03)
p.charcode("MULTILINGUAL")

password = randomword(6)

t = tabCompleter()
t.createListCompleter(usernames)
readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")
readline.set_completer(t.listCompleter)
username = input("Suche Benutzer: ").replace(" ", "")
print(username)

if hasUser(users, username):
	print("Updating user: " + username)
	data = {'idUsername': username, 'password': password }
	q = session.post("http://" + sys.argv[1] + '/api/user/update', json=data).text
	print(q)
	print("Passwort: " + password)
	printInfo(username, password)

else:
	print("Der Benutzer " + username + " existiert nicht!")


