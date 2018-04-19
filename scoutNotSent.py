#!/usr/bin/python
import os
import json
import pyrebase
from slackclient import SlackClient

#Defines the path to the user for use later
home = os.path.expanduser('~')

#Sets up the firebase
url = 'scouting-2018-houston'

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
currentCycle = db.child('cycleCounter').get().val()

#Finds all of the tempTIMDs in the sent folder
timds = list(db.child("TempTeamInMatchDatas").shallow().get().val())
dTimds = [x for x in timds if int(x.split("Q")[1].split("-")[0]) == currentMatch-2]
diagnostics = {}
diagnostics['mode'] = {int(dTimds[ix].split("-")[1]):db.child("TempTeamInMatchDatas/"+str(dTimds[ix])+"/mode").get().val() for ix in range(len(dTimds))}
diagnostics['cycle'] = {int(dTimds[ix].split("-")[1]):db.child("TempTeamInMatchDatas/"+str(dTimds[ix])+"/cycle").get().val() for ix in range(len(dTimds))}
diagnostics['names'] = {int(dTimds[ix].split("-")[1]):db.child("TempTeamInMatchDatas/"+str(dTimds[ix])+"/scoutName").get().val() for ix in range(len(dTimds))}
print("Done getting data from firebase.") 

def getNameFromID(i):
	return str(diagnostics['names'][i]) if diagnostics['cycle'][i] == currentCycle else str(diagnostics['names'][i])+"*"

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
	for match in range(1, currentMatch-1):
		if match not in sent:
			scoutNotSent[scout] += [match]

#Creates a string for slack based on scoutNotSent
slackScoutNotSent = ''
for num in expected:
	sent = scoutNotSent[num]
	if sent:
		slackScoutNotSent += ('Scout ' + str(num) + " (" + getNameFromID(num)+'): ')
		for match in sent:
			slackScoutNotSent += str(match)
			if match != sent[-1]:
				slackScoutNotSent += ', '			
		slackScoutNotSent += '\n'

diagnosticsMessage = ''

modeMode = max(set(list(diagnostics['mode'].values())), key=list(diagnostics['mode'].values()).count)
modeMode = None if not list(diagnostics['mode'].values()).count(modeMode) > 1 else modeMode

modeCycle = max(set(list(diagnostics['cycle'].values())), key=list(diagnostics['cycle'].values()).count)
modeCycle = None if not list(diagnostics['cycle'].values()).count(modeCycle) > 1 else modeCycle

if modeMode == None:
	diagnosticsMessage += "Please check mode on all tablets.\n"
elif list(diagnostics['mode'].values()).count(modeMode) != len(diagnostics['mode']):
	diagnosticsMessage += "> Current detected mode: " + str(modeMode) + "\n"
	for k, v in diagnostics['mode'].items():
		if v != modeMode:
			diagnosticsMessage += ('Scout ' + str(k) + " (" + getNameFromID(k)+'): ') + str(v) + "\n"

if modeCycle == None:
	diagnosticsMessage += "Please check cycle on all tablets.\n"
elif list(diagnostics['cycle'].values()).count(modeCycle) != len(diagnostics['cycle']):
	diagnosticsMessage += "> Current detected cycle: " + str(modeCycle) + "\n"
	for k, v in diagnostics['cycle'].items():
		if v != modeCycle:
			diagnosticsMessage += ('Scout ' + str(k) + " (" + getNameFromID(k)+'): ') + str(v) + "\n"


#diagnosticsMessage = ''

status = '#f1ad1d'
if slackScoutNotSent == '' and diagnosticsMessage == '':
	slackScoutNotSent = 'All scouts have sent.'
	status = 'good'
elif diagnosticsMessage != '' and slackScoutNotSent == '':
	slackScoutNotSent = diagnosticsMessage
elif diagnosticsMessage != '' and slackScoutNotSent != '':
	slackScoutNotSent = slackScoutNotSent + '\n' + diagnosticsMessage


#Gets slack API key
with open(os.path.join(home, 'Downloads/data/apikey.txt'), 'r') as f:
	apikey = f.read()

slack = SlackClient(apikey)

userIDs = [
	#'U749CSZ36', # Carl
	'U1R1L8J9H', # Sam Chung
	'U2UPNHSFK', # Sam Sands
	'U2VQ47JN7', # Gemma
]

#Sends a message to every user
for user in userIDs:
	print(slack.api_call('chat.postMessage',
		channel = user,
		as_user = True,
		icon_url = 'https://i.imgur.com/1snON7W.png',
		attachments = [{'pretext':'Match '+str(currentMatch-2)+' SNS',
			'fallback': 'Match '+str(currentMatch-2)+' SNS',
			'color':status, 'text':slackScoutNotSent,
		}]
	))
print("Sent SNS notifications.")