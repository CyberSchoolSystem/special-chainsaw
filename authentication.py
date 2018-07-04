import mechanize

br=mechanize.Browser()
br.open('http://localhost:3000/auth/login')
br.select_form(nr=0)

br["username"] = "jesus"
br["password"] = "123"
br.submit()

br.retrieve('http://localhost:3000/vote/terminated', 'file')
