#!/usr/local/bin/python

import os
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

doc = SimpleDocTemplate("Benutzerliste.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
doc.pagesize = portrait(A4)
elements = []

pdfmetrics.registerFont(TTFont('monospace', 'monospace.ttf'))

def gen_password(length=6, charset="ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghjkimnopqrstuvwxyz0123456789."):
    random_bytes = os.urandom(length)
    len_charset = len(charset)
    indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
    return "".join([charset[index] for index in indices])


data = [["Klasse", "Name", "Benutzername", "Passwort"]]

f = open('userliste.csv','w')

with open('schulerliste.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        password = gen_password()
        name = row[1] + " " + row[2]

        print(name + ": " + password)
        f.write(row[4] + ";" + name + ";" + row[0] + ";" + password + "\n")
        data.append([row[4], name, row[0], password])



#TODO: Get this line right instead of just copying it from the docs
style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('TEXTFONT', (0, 0), (-1, -1), 'monospace'),
                       ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
                       ('BACKGROUND',(0,0),(-1,-1),colors.white)
                       ])

#Configure style and word wrap
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
data2 = [[Paragraph(cell, s) for cell in row] for row in data]
t=Table(data2)
t.setStyle(style)
#Send the data and build the file
elements.append(t)
doc.build(elements)
