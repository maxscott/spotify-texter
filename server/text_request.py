#!/usr/bin/python

import sys
import cgi
import MySQLdb
import json
import datetime
import httplib
import cgitb; cgitb.enable()
form = cgi.FieldStorage()

body = str(form.getfirst("Body", ""))
smsid = str(form.getfirst("SmsSid", ""))
acctid = str(form.getfirst("AccountSid", ""))
fromnum = str(form.getfirst("From", ""))
tonum = str(form.getfirst("To", ""))

fromnum = fromnum.replace("+", "")
tonum = tonum.replace("+", "")

body = body.replace("'", "")
body = body.replace("(", "")
body = body.replace(")", "")

if 'fuck' in body:
	body = fromnum + " likes dirty words..."
elif 'Fuck' in body:
	body = fromnum + " likes dirty words..."

# connect
db = MySQLdb.connect(host="localhost", user="root", passwd="root",db="MaxIsCool")
cursor = db.cursor()

# confirm its a real number
cursor.execute('''select distinct(Number) from TwilioNumbers''')
rownum = int(cursor.rowcount)

# look for match
for i in range(0, rownum):
	row = cursor.fetchone()
	plusone = "1"+tonum
	if tonum == row[0]:
		break
	elif  plusone == row[0]:
		tonum = plusone
		break
	elif i == (rownum-1):
		#sys.exit("Wrong number!? ")
		q = 0
# query
values = [tonum, fromnum, body, str(0), str(datetime.datetime.now())]

message = ""

if body == "?":
	query = "select CurrentState from TwilioNumbers where Number = " + tonum;
	cursor.execute(query)
	message = str(cursor.fetchone()[0])
else:
	query = "insert into Requests (ToNumber, FromNumber, Message, Requests.Read, TimeSent) values ( '" + "','".join(values) + "')"
	cursor.execute(query)
	message = str(body) + '. ' + ' noted. '

print "Content-Type: application/xml"
# print 
# print "<html>"
# print "<body>"
# print q
# print values
# print query
# print "</body>"
# print "</html>"


	
# # print '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
print """
<Response>
<Sms>
"""
print message
print """
</Sms>
</Response>
"""