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

# columns
collist = ["RequestId", "ToNumber", "FromNumber", "Message", "Read", "TimeSent"]

selectList = ",".join(collist);

# query
helperquery = """
select r.RequestId, r.ToNumber, r.FromNumber, r.Message, r.Read, r.TimeSent 
from Requests r join TwilioNumbers t 
on r.ToNumber = t.Number"""

statusquery = ""

# get unread messages from a valid (specific) ToNumber)
if request.has_key('twilionumber'):
	pullquery = helperquery + " where t.Number = '" + str(request['twilionumber'].value) + "' and r.Read = 0"	
	if request.has_key('status'):
		statusquery = "update TwilioNumbers set CurrentState = '" + str(request['status'].value) + "' where Number = '" + str(request['twilionumber'].value) + "'"
		cursor.execute(statusquery)
else:
	pullquery = helperquery + " where r.Read = 0"

cursor.execute(pullquery)
	
numrows = int(cursor.rowcount)

# Process each message as
commands = ["pause", "Pause"]
normalrow = []
commandrows = []
updatethese = []

for x in range(0,numrows):
	temprow = allStrings(cursor.fetchone())
	updatethese.append(temprow[0])
	if temprow[3] in commands:
		commandrows.append(",".join(temprow))
	else:
		normalrow.append(",".join(temprow))

# update the read rows
if numrows > 0:
	newquery = "update Requests set Requests.Read = 1 where RequestId in (" + str(",".join(updatethese)) + ")"
	cursor.execute(newquery)

# JSON
print "Content-Type: application/json"
print
print json.dumps({"Songs":normalrow, "Commands":commandrows}, indent=2)

# print "Content-Type: text/html"
# print
# print "<html>"
# print "<body>"
# print statusquery
# print "</body>"
# print "</html>"