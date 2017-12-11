## SI 206 2017
## Final Project
## Name: Suhas Maganti

import json
import sqlite3
import requests
import urllib3
from instagram.client import InstagramAPI
import facebook





####Instagram
client_id = "a5614a76dca6446c8c49ab793b3769fe"
client_secret = "f2f7a1804b584bc69f11628e42d5c385"
redirect_uri = "https://www.google.com/"
scope = ['basic', 'comments', 'follower_list', 'likes', 'public_content']
code = "c1fe9c41659740f09fc110fcb7e6870b"

insta_token = "1420219052.a5614a7.7f67441564634eb5bf0805513e6fd89a"

web_request = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token={}'.format(insta_token))
insta_data = web_request.json()

####Facebook
fb_token = "EAACEdEose0cBAFlzjqjT3KOKRDZBiddKSKiwGr0iDcGcG2bJv20Gh5WKeztESwiXUxRBlWxjj66XnJQnK6wR06l8jybWJa5FpLbe6S1CG58t0CNfqEbm8oAsIK6HhnwuRKD1h8fjMwmLB19ZAZCNLwmG9ZCW7xN2ZAZAxfgZBQqLy9Lwgqyy7gwBZCXVVHQvK8sIALoEfzLsWgZDZD"


graph = facebook.GraphAPI(access_token=fb_token, version = 2.7)
friends = graph.get_connections(id='me', connection_name='friends')


def get_hometown(user_id):
	try:
		hometown = graph.get_object(id=user_id, fields='hometown')
		return(hometown['hometown']['name'])
	except:
		return('')

def get_location(user_id):
	try:
		hometown = graph.get_object(id=user_id, fields='location')
		return(hometown['location']['name'])
	except:
		return('')

def get_gender(user_id):
	try:
		gender = graph.get_object(id=user_id, fields='gender')
		return(gender['gender'])
	except:
		return('')



####Caching setup

CACHE_FNAME = "FinalProject_cache.json"

try:
    cache_file = open(CACHE_FNAME, 'r') # Read the data from the file
    cache_contents = cache_file.read()  # Make it into a string, if it's there
    CACHE_DICTION = json.loads(cache_contents) # Put it in dictionary
    cache_file.close() # Close the file
except:
    CACHE_DICTION = {}

try:
	insta_cache= json.dumps(insta_data)
	fb_cache = json.dumps(friends)
	fw = open(CACHE_FNAME,"w")
	fw.write(insta_cache)
	fw.write("\n")
	fw.write(fb_cache)
	fw.close() # Close the open file
except:
	None

"""
####Creating a table in SQLite3

conn = sqlite3.connect('FinalProject.sqlite', timeout = 5)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Instagram
	(pic_id text PRIMARY KEY,
		caption text,
		likes integer,
		comments integer)''')


for i in range(20):
	pic_id = insta_data['data'][i]['id']
	caption = insta_data['data'][i]['caption']['text']
	likes = insta_data['data'][i]['likes']['count']
	comments = insta_data['data'][i]['comments']['count']

	cur.execute("INSERT OR IGNORE INTO Instagram (pic_id, caption, likes, comments) VALUES (?,?,?,?)",
	(pic_id, caption, likes, comments))
	


cur.execute('''CREATE TABLE IF NOT EXISTS Facebook 
	(name text PRIMARY KEY,
		user_id integer,
		gender text,
		hometown text,
		location text)''')

for i in range(25):
	name = friends['data'][i]['name']
	user_id = friends['data'][i]['id']
	gender = get_gender(user_id)
	hometown = get_hometown(user_id)
	location = get_location(user_id)

	cur.execute("INSERT OR IGNORE INTO Facebook (name, user_id, gender, hometown, location) VALUES (?,?,?,?,?)",
	(name, user_id, gender, hometown, location))

conn.commit()
cur.close()
"""












