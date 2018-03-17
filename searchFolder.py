import os
import json
import pyrebase

import traceback
from slackclient import SlackClient

home = os.path.expanduser('~')

with open(os.path.join(home, 'Downloads/data/apikey.txt'), 'r') as f:
	apikey = f.read()

slack = SlackClient(apikey)
userIDs = [
	'U749CSZ36', # Carl
	'U1R1L8J9H', # Sam
]

# This entire try/except statement physically pains me. Blame Sam.
try:
	url = 'servervartest-2018'
	#url = 'scouting-2018-9023a'

	config = {
		'apiKey': 'mykey',
		'authDomain': url + '.firebaseapp.com',
		'databaseURL': 'https://' + url + '.firebaseio.com/',
		'storageBucket': url + '.appspot.com'
	}

	firebase = pyrebase.initialize_app(config)
	db = firebase.database()

	path = os.path.join(home, 'Downloads')
	
	# Searches for files in 'path' folder
	for file in os.listdir(path):
		# Checks if file is a .jsontxt file
		if file.endswith(".jsontxt"):
			# Adds file path to file name instead of using string addition
			fullPath = os.path.join(path, file)
			# Opens file, imports json data
			with open(fullPath, 'r') as f:
				data = json.load(f)
			# Takes TIMDname from file data (top level key, only one)
			TIMDname = [x for x in data][0]
			# Uploads TIMD to firebase
			db.child('TempTeamInMatchDatas/'+TIMDname).set(data[TIMDname])
			print('Uploaded %s.' % TIMDname)
			# Moves uploaded files to 'sent' folder to avoid re-upload
			os.rename(fullPath, os.path.join(path, 'sent/', file))
		# Removes files that aren't .txt's or directories
		# If statement to ignore directories
		elif os.path.isfile(os.path.join(path, file)):
			os.remove(os.path.join(path, file))
except Exception as e:
	title = 'ERROR: ' + str(e)
	error = traceback.format_exc()
	print(error)
	for user in userIDs:
		slack.api_call('chat.postMessage',
			channel = user,
			as_user = True,
			text = error,
		)
