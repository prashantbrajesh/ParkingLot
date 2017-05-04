#!/usr/bin/python
import sqlite3

try:
	conn = sqlite3.connect('test.db')
	print "Opened DB success"

	conn.execute("Insert into Company ")
	conn.close()
except Exception as e:
	print str(e)

