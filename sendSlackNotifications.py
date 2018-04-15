#!/usr/bin/python
from slackclient import SlackClient
import pyrebase
import os

home = os.path.expanduser('~')

with open(os.path.join(home, 'Downloads/data/apikey.txt'), 'r') as f:
	apikey = f.read()
slack = SlackClient(apikey)

url = 'scouting-2018-temp'

config = {
	'apiKey': 'mykey',
	'authDomain': url + '.firebaseapp.com',
	'databaseURL': 'https://' + url + '.firebaseio.com/',
	'storageBucket': url + '.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

currentMatch = db.child('currentMatchNum').get().val()
slackProfiles = db.child('activeSlackProfiles').get().val()

notifications = {}
for user in slackProfiles:
	if slackProfiles[user].get('notifyInAdvance', None) != None:
		notifications[user] = [x for x in slackProfiles[user]['starredMatches'] if x >= currentMatch and (x-currentMatch <= slackProfiles[user]['notifyInAdvance'])]

for user in notifications:
	text = ""
	for match in notifications[user]:
		if match-currentMatch == 0:
			text += 'Match '+str(match)+' is next.\n'
		elif match-currentMatch == 1:
			text += 'Match '+str(match)+' is 1 match away.\n'
		else:
			text += 'Match '+str(match)+' is '+str(match-currentMatch)+' match(es) away.\n'
	if text != "":
		text = text[:-1]
		print(slack.api_call('chat.postMessage',
			channel = user,
			as_user = True,
			text = text,
			))