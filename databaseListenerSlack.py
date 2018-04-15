#!/usr/bin/python -p
import os
import pyrebase
import subprocess

home = os.path.expanduser('~')

url = 'scouting-2018-temp'

config = {
	'apiKey': 'mykey',
	'authDomain': url + '.firebaseapp.com',
	'databaseURL': 'https://' + url + '.firebaseio.com/',
	'storageBucket': url + '.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def stream_match_handler(message):
	if type(message["data"]) == int:
		with open(os.path.join(home, 'Downloads/data/lastSentMatch.txt'), 'r') as f:
			cycle = f.read()
		if cycle == "":
			cycle = 0
		if message["data"] != int(cycle) and home == "/home/citrus": # Prevents double slack notification
			isubprocess.call(os.path.join(home, "scoutManager/sendSlackNotifications.py"), shell=True)
			with open(os.path.join(home, 'Downloads/data/lastSentMatch.txt'), 'w') as f:
				f.write(str(message["data"]))

stream3 = db.child("currentMatchNum").stream(stream_match_handler)