#!/usr/bin/env python
import csv
import random
import copy
import smtplib
from sets import Set
from email.mime.text import MIMEText

gmail_user = ''
gmail_pwd = ''
infile = 'NamesEmails.csv'

class Participant:
    def __init__(self,name,email):
        self.name = name
        self.email = email
    def __hash__(self):
        return hash(self.email)
    def __str__(self):
        return self.name
    def __eq__(self,other):
        return self.name == other.name and self.email == other.email
    def __ne__(self,other):
        return not (self == other)

givers = Set()
receivers = Set()
with open(infile,"rb") as email_csv:
    reader = csv.reader(email_csv)
    for row in reader:
        p = Participant(row[0],row[1])
        givers.add(p)
        receivers.add(p)

assignments = [] #list of 2-tuples (giver, receiver)

for giver in givers:
    themself = Set([giver])
    if len(receivers - themself) > 0:
        receiver = random.sample(receivers - themself , 1)[0]
    else:
        #last person stuck with themself switch assignments with a random person
        receiver = receivers.pop()
        randomAssignment = random.choice(assignments)
        receiver, randomAssignment[1] = randomAssignment[1],receiver
    assert (giver != receiver), "self assignment"
    assignments.append([giver,receiver])
    receivers.discard(receiver)

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
except:
    print "failed to connect to server"
    raise
for assignment in assignments:
    message_text = "{}, your assignment is {}".format(str(assignment[0]),str(assignment[1]))
    msg = MIMEText(message_text)
    msg['Subject'] = 'Secret Santa Assignment'
    msg['From'] = gmail_user
    msg['To'] = getattr(assignment[0],'email')
    try:
        server.sendmail(gmail_user, getattr(assignment[0],'email'), msg.as_string())
    except:
        print "failed to send email"
        raise
server.close()
print 'success'
