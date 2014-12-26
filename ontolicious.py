import json
import urllib2
import md5
import time
from datetime import datetime
import MySQLdb
from secrets import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

db = MySQLdb.connect(host=MYSQL_HOST, # your host, usually localhost
                     user=MYSQL_USER, # your username
                      passwd=MYSQL_PASSWORD, # your password
                      db=MYSQL_DB) # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

def fix_unicode(str):
	return str.encode('ascii', 'ignore')

def remove_characters(str):
	return str.replace("'", '')

def insert_entry(entry):
	entry[3] = remove_characters(entry[3][0:254])
	entry[1] = remove_characters(entry[1])
	cur.execute("select * from tags where triple_md5 = '" + entry[5] + "'")
	if cur.fetchone() is None:
		try:
			cur.execute("insert into tags (" \
							"user, url, url_md5, tag, tag_date, triple_md5, source, user_url_md5) values (" + \
							"'"    + entry[0] + \
							"', '" + entry[1] + \
							"', '" + entry[2] + \
							"', '" + entry[3] + \
							"', '" + entry[4] + \
							"', '" + entry[5] + \
							"' ,'" + entry[6] + \
                                                        "' ,'" + entry[7] + \
							"')" + \
						";")
		except Exception as e:
			print e, entry

def parse_feed(data, source):
	entries = []
	user_set, url_set, tag_set = [], [], []
	for d in data:
		user			= fix_unicode(d['a'])
		url 			= fix_unicode(d['u'])
		url_md5			= md5.md5(url).hexdigest()
		tags			= d['t']
		tag_date		= fix_unicode(d['dt'])
		user_url_md5		= md5.md5(user + url).hexdigest()
		source			= source
		user_set.append(user)
		url_set.append(url)
		for tag in tags:
			tag 		= fix_unicode(tag)
			if tag:
				tag_set.append(tag)
			triple_md5	= md5.md5(user + url + tag).hexdigest()
			entry 		= [
							user
							,url
							,url_md5
							,tag
							,tag_date
							,triple_md5
							,source
							,user_url_md5
						  ]
			entries.append(entry)
	user_set			= set(user_set) 
	url_set 			= set(url_set)
	tag_set				= set(tag_set)
	return entries, user_set, url_set, tag_set

print "start: " + str(datetime.now())

for _ in range(1000):
	url 				= "http://feeds.delicious.com/v2/json/popular?count=100"
	data 				= parse_feed(json.load(urllib2.urlopen(url)), "popular")
	popular_entries 	= data[0]
	popular_user_set 	= data[1]
	popular_url_set		= data[2]
	popular_tag_set		= data[3]

	for popular_entry in popular_entries:
		try:
			if popular_entry[3] != '': 
				insert_entry(popular_entry)
		except Exception as e:
			print e

	for user in popular_user_set:
		if user:
			url = "http://feeds.delicious.com/v2/json/" + user  + "?count=100"
			user_data = parse_feed(json.load(urllib2.urlopen(url)), "user")
			for user_entry in user_data[0]:
				try:
					if user_entry[3] != '': 
						insert_entry(user_entry)
				except Exception as e:
					print e
		#print "pause, " + user + " done."
		cur.execute("commit;")
		time.sleep(10)
	cur.execute("select count(*) from tags;")
	print "cycle completed: " + str(datetime.now()) + ", record count: " + str(cur.fetchone()[0])
	time.sleep(120)

print "done."
