## SI 206 2017
## Final Project
## Name: Suhas Maganti

import json
import sqlite3
import requests
import urllib3
import api_info
from instagram.client import InstagramAPI
import facebook
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *
import datetime

print("Suhas Maganti SI 206 Final Project", "\n")
print("Start!")
print("Accessing API...")

####Instagram
client_id = api_info.client_id
client_secret = api_info.client_secret
redirect_uri = api_info.redirect_uri
code = api_info.code
insta_token = api_info.insta_token

web_request = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token={}'.format(insta_token))
insta_data = web_request.json()


####Facebook
try:
	fb_token = api_info.fb_token

#Accessing the api
	graph = facebook.GraphAPI(access_token=fb_token, version = 2.7)
	friends = graph.get_connections(id='me', connection_name='friends')

#Facebook functions to get hometown, location and gender

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

	gender_dic = {'male': 0, 'female': 0}	#Dic to collect gender data for graphs
	facebook_list = []

	for i in range(25):
		facebook_dic = {}
		name = friends['data'][i]['name']
		facebook_dic['name'] = name
		user_id = friends['data'][i]['id']
		facebook_dic['user_id'] = user_id 
		gender = get_gender(user_id)
		facebook_dic['gender'] = gender 
		if gender == 'male':
			gender_dic['male'] += 1
		else:
			gender_dic['female'] += 1
		hometown = get_hometown(user_id)
		facebook_dic['hometown'] = hometown 
		location = get_location(user_id)
		facebook_dic['location'] = location
		facebook_list.append(facebook_dic)

	print("Facebook api: Success")
except:
	print("Facebook api: Failed")
	print("Using cached data")
####Caching setup

CACHE_FNAME = "FinalProject_cache.json"

try:
    cache_file = open(CACHE_FNAME, 'r') # Read the data from the file
    cache_contents = cache_file.read()  # Make it into a string, if it's there
    CACHE_DICTION = json.loads(cache_contents) # Put it in dictionary
    cache_file.close() # Close the file
except:
    CACHE_DICTION = {}

def check_insta(insta):
	if insta in CACHE_DICTION:
		return CACHE_DICTION[insta]
	else:
		try:
			data = insta_data['data']	#Gets Instagram data
			CACHE_DICTION[insta] = data
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME,"w")	#Opens cache file
			fw.write(dumped_json_cache)	#Write data
			fw.close() # Close the open file
			return CACHE_DICTION[insta]
		except:
			return None

def check_fb(fb):
	if fb in CACHE_DICTION:
		return CACHE_DICTION[fb]
	else:
		try:
			data = facebook_list	#Gets Facebook data
			CACHE_DICTION[fb] = data
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME,"w")	#Open cache file
			fw.write(dumped_json_cache)	#Write data
			fw.close() # Close the open file
			return CACHE_DICTION[fb]
		except:
			return None

####Creating a table in SQLite3

conn = sqlite3.connect('FinalProject.sqlite', timeout = 5)
cur = conn.cursor()

#Create Instagram Table
cur.execute('''CREATE TABLE IF NOT EXISTS Instagram
	(pic_id text PRIMARY KEY,
		posted text,
		caption text,
		likes integer,
		comments integer)''')

#Access data
insta_captions  =[]		#Lists for graph keys
insta_likes = [] 		#Lists for graph data
insta_comments = []		#Lists for graph data
gender_dic = {'male': 0, 'female': 0}

try:
	for i in range(20):
		data = check_insta('data')
		pic_id = data[i]['id']
		time = data[i]['created_time']
		posted = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d')
		caption = data[i]['caption']['text']
		insta_captions.append(caption)
		likes = data[i]['likes']['count']
		insta_likes.append(likes)
		comments = data[i]['comments']['count']
		insta_comments.append(comments)

#Input data into table
		cur.execute("INSERT OR IGNORE INTO Instagram (pic_id, posted, caption, likes, comments) VALUES (?,?,?,?,?)",
		(pic_id, posted, caption, likes, comments))
	print("Generate Instagram Table: Success")

except:
	print("Generate Instagram Table: Failed")

#Create Facebook Table	
cur.execute('''CREATE TABLE IF NOT EXISTS Facebook 
	(name text PRIMARY KEY,
		user_id integer,
		gender text,
		hometown text,
		location text)''')

#Access data
try:
	for i in range(25):
		fb = check_fb('fb')
		name = fb[i]['name']
		user_id = fb[i]['user_id']
		gender = fb[i]['gender']
		if gender == 'male':
			gender_dic['male'] += 1
		else:
			gender_dic['female'] += 1
		hometown = fb[i]['hometown']
		location = fb[i]['location']

#Input data into table	
		cur.execute("INSERT OR IGNORE INTO Facebook (name, user_id, gender, hometown, location) VALUES (?,?,?,?,?)",
		(name, user_id, gender, hometown, location))
	print("Generate Facebook Table: Success")
except:
	print("Generate Facebook Table: Failed")


conn.commit()
cur.close()

####Plotly Graphing
####Instagram Likes and Comments Graph

#Replacing newline characters with a space
updated_insta_captions = []
for i in insta_captions:
	new_caption = i.replace("\n"," ")
	updated_insta_captions.append(new_caption) 

#print(insta_captions)
plotly_api = api_info.api_key
plotly.tools.set_credentials_file(username='suhasmaganti', api_key=plotly_api)

try:
	trace1 = go.Bar(
    	x=updated_insta_captions,
    	y=insta_likes,
    	name='Likes'
	)
	trace2 = go.Bar(
    	x=updated_insta_captions,
    	y=insta_comments,
    	name='Comments'
	)

	data = [trace1, trace2]
	layout = go.Layout(
    	barmode='group'
	)

	fig = go.Figure(data=data, layout=layout)
	py.iplot(fig, filename='Instagram')
	print("Generate Instagram Graph: Success")
except:
	print("Generate Instagram Graph: Failed")
####Facebook Gender Pie Chart
try:
	labels = ['Male','Female']
	values = list(gender_dic.values())

	trace = go.Pie(labels=labels, values=values)

	py.iplot([trace], filename='Facebook Gender')
	print("Generate Facebook Graph: Success")
except:
	print("Generate Facebook Graph: Failed")

print("Done!", "\n")
print("Instagram Graph: https://plot.ly/~suhasmaganti/2")
print("Facebook Graph: https://plot.ly/~suhasmaganti/4")

####THE END

