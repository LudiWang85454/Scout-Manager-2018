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

print("Getting data from firebase...")
#Finds the number of matches already played using the currentMatchNum key
currentMatch = db.child('currentMatchNum').get().val()

#Finds all of the tempTIMDs in the sent folder
timds = list(db.child("TempTeamInMatchDatas").shallow().get().val())
print("Done getting data from firebase.")

#Finds all of the scouts who are supposed to be sending to cross reference with
expected = [x for x in range(1,19)]

#Initializes the dictionary used for the scoutNotSent function
scoutSent = {}
scoutNotSent = {}

for scout in expected:
	scoutSent[scout] = []
	scoutNotSent[scout] = []

for timd in timds:
	if 'Q' in timd:
		idAndMatch = timd.split('Q')[1]
		match = idAndMatch.split('-')[0]
		scoutNum = idAndMatch.split('-')[1]
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

status = 'warning'
if slackScoutNotSent == '':
	slackScoutNotSent = 'All scouts '+str(min(expected))+'-'+str(max(expected))+' sent.'
	status = 'good'

#Gets slack API key
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
			as_user = True,
			icon_url = 'https://i.imgur.com/1snON7W.png',
			attachments = [{'pretext':'Match '+str(currentMatch)+' SNS | Scouts '+str(min(expected))+'-'+str(max(expected)),
				'fallback': 'Match '+str(currentMatch)+' SNS',
				'color':status, 'text':slackScoutNotSent
			}]
		)
