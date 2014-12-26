import json
import urllib2
import md5
import time
from datetime import datetime
import MySQLdb
from metadata_parser import MetadataParser
import requests
from secrets import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST

def fix_unicode(str):
	pass

def remove_characters(input):
	if input is None:
		return 	''
	else:
		input = input.encode("utf8","ignore")
		input = str(input)
		input = input.replace("'", '')
		input = input.replace("\\", '')
		return 	input

db = MySQLdb.connect(host 	=MYSQL_HOST, # your host, usually localhost
                     user 	=MYSQL_USER, # your username
                     passwd 	=MYSQL_PASSWORD, # your password
                     db		=MYSQL_DB) # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

sql = "select url, count(*) from tags " \
	  "where url_md5 not in " \
	  	"(select distinct url_md5 from url_meta) " \
	  "group by url order by count(*) desc;"

cur.execute(sql)
urls = cur.fetchall()

i = 0
for url in urls:
	i = i + 1
	url 				= remove_characters(url[0])
	try:	
		headers 		= {
		    				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
		    				'From': 'admin@ontolicio.us'  # This is another valid field
						  }
		page 			= MetadataParser(url=url, requests_timeout=5, url_headers=headers)
		title 			= remove_characters(page.get_metadata('title'))
		url_resolved 	= remove_characters(page.get_metadata('url'))
		image 			= remove_characters(page.get_metadata('image'))
		description 	= remove_characters(page.get_metadata('description'))

		sql 			= "insert into url_meta (title, description, url, url_md5, image) " \
			  			  "values ('" + title + "', '" + description + "', '" + url_resolved + "', md5('" + url + "'), '" + image + "');"
	except Exception as e:
		e 				= remove_characters(str(e))
		sql 			= "insert into url_meta (title, description, url, url_md5, image) " \
			  			  "values ('error', '" + e + "', '" + url + "', md5('" + url + "'), '');"
	finally:
		cur.execute(sql) 
		cur.execute("commit;")
		if i % 100 == 0: print i

time.sleep(120)
quit();
