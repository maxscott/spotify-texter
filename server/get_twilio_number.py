#!/usr/bin/python

import MySQLdb
import json
import cgi
import datetime
import httplib
import cgitb; cgitb.enable()

# replace dates with strings
def cleanDates(row):
	row2 = {}
	for x in range(0,len(row)):
		if(type(row[x]) == datetime.datetime):		
			row2[collist[x]] = str(row[x])
		else:
			row2[collist[x]] = row[x]
	return row2

# connect and query
def mySqlCursor():
	db = MySQLdb.connect(host="localhost", user="root", passwd="root",db="MaxIsCool")
	return db.cursor()

cursor = mySqlCursor()	
	
collist = ["Number", "ExpireTime", "QueueSize", "Password", "CurrentHost"]
selectList = ",".join(collist);
cursor.execute('''select ''' + selectList + ''' from TwilioNumbers where CurrentHost is null''')

row = cursor.fetchone()
row2 = cleanDates(row)

beginning = """{
\"TwilioNumbers\": [
""";
ending = """]
}""";	
		
print "Content-Type: application/json"
print
print json.dumps(row2, indent=2)