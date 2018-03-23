import os
import json
import pyrebase
from slackclient import SlackClient

#Defines the path to the user for use later
home = os.path.expanduser('~')

#Sets up the firebase
url = 'scouting-2018-9023a'

config = {
	'apiKey': 'mykey',
	'authDomain': url + '.firebaseapp.com',
	'databaseURL': 'https://' + url + '.firebaseio.com/',
	'storageBucket': url + '.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#Finds the number of matches already played using the currentMatchNum key
currentMatch = db.child('currentMatchNum').get().val()

#Gets the activeScouts file from data
with open(os.path.join(home, 'Downloads/data/activeScouts.json'), 'r') as f:
	devices = json.load(f)

#Finds all of the scouts who are supposed to be sending to cross reference with
expected = sorted([int(device.split('t')[1]) for device in devices.keys()])

#Initializes the dictionary used for the scoutNotSent function
scoutSent = {}
scoutNotSent = {}

for scout in expected:
	scoutSent[scout] = []
	scoutNotSent[scout] = []

#Finds all of the tempTIMDs in the sent folder
stt = os.listdir(os.path.join(home, 'Downloads/sent/'))

#Deletes timestamps and the jsontxt ending
for timd in stt:
	index = stt.index(timd)
	stt[index] = timd.split('.')[0]
	if '_' in timd:
		stt[index] = stt[index].split('_')[1]

	#Adds scout numbers to the scoutSent list
	timd = stt[index]
	if 'Q' in timd:
		teamAndMatch = timd.split('-')[0]
		scoutNum = timd.split('-')[1]
		match = teamAndMatch.split('Q')[1]
		scoutSent[int(scoutNum)] += [int(match)]

#Finally, it iterates through all of the matches in scoutSent and finds missing scouts
for scout, sent in scoutSent.items():
	for match in range(1, currentMatch):
		if match not in sent:
			scoutNotSent[scout] += [match]

#Creates a string for slack based on scoutNotSent
slackScoutNotSent = ''
for num in expected:
	sent = scoutNotSent[num]
	if sent:
		slackScoutNotSent += ('Scout ' + str(num) + ': ')
		for match in sent:
			slackScoutNotSent += str(match)
			if match != sent[-1]:
				slackScoutNotSent += ', '			
		slackScoutNotSent += '\n'

#Finds Users who want scoutNotSent on slack
with open(os.path.join(home, 'Downloads/data/apikey.txt'), 'r') as f:
	apikey = f.read()

slack = SlackClient(apikey)

userIDs = [
	'U749CSZ36', # Carl
	'U1R1L8J9H', # Sam
]

#Sends a message to every user
for user in userIDs:
		slack.api_call('chat.postMessage',
			channel = user,
			as_user = False,
			text = slackScoutNotSent,
			username = 'Scouts To Yell At Bot',
			icon_url = 'https://i.imgur.com/1snON7W.png'
		)
