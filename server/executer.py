#!/usr/bin/python

import MySQLdb
import json
import cgi
import datetime
import httplib
import cgitb; cgitb.enable()
request = cgi.FieldStorage()

def allStrings(row):
	row2 = []
	for x in range(0,len(row)):
		row2.append(str(row[x]))
	return row2

# connect
db = MySQLdb.connect(host="localhost", user="root", passwd="root",db="MaxIsCool")
cursor = db.cursor()

query =  str(request['Body'].value)
cursor.execute(query)

messages = []
rownum = int(cursor.rowcount)

for i in range(0, rownum):
	messages.append(", ".join(allStrings(cursor.fetchone())))

print "Content-Type: application/xml"
print """
<Response>
<Sms>
"""
print "/n".join(messages)
print """
</Sms>
</Response>
"""