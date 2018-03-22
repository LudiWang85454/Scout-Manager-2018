import bluetooth
from PyOBEX.client import Client
import pyrebase
import os
import json
import random
import sys

resendMode = 0

resendIDs = []

if len(sys.argv) == 3:
	if sys.argv[1] == 'resend':
		resendMode = 1
		resendIDs = [int(x) for x in list(sys.argv[2])]

home = os.path.expanduser('~')

url = 'scouting-2018-9023a'

config = {
	'apiKey': 'mykey',
	'authDomain': url + '.firebaseapp.com',
	'databaseURL': 'https://' + url + '.firebaseio.com/',
	'storageBucket': url + '.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

with open(os.path.join(home, 'Downloads/data/activeScouts.json'), 'r') as f:
	devices = json.load(f)

if resendMode == 1:
	devices = {k:v for k,v in devices.iteritems() if int(k[5:]) in resendIDs}

print(devices)

# Backup assignment system
'''
scouts = 'Nathan Justin Joey Noah Anoushka Zoe Rolland Teo Hanson Jack Tim Calvin Asha'
#scouts = 'Zach James Gemma Carl Freddy Carter Kenny Emily Eli Stephen Aidan Lyra Aakash Amanda'
scouts = scouts.split()

with open(os.path.join(home, 'Documents/dallasIndex.json'), 'r') as f:
	matchIndex = json.load(f)
# Using for scout training until full system implemented

with open(os.path.join(home, 'Documents/matches_dallas2018.json'), 'r') as f:
	matchData = json.load(f)
index = matchIndex[str(matchNum)]
redTeams = matchData[index]['alliances']['red']['team_keys']
redTeams = [int(team[3:]) for team in redTeams]
blueTeams = matchData[index]['alliances']['blue']['team_keys']
blueTeams = [int(team[3:]) for team in blueTeams]
teams = redTeams + blueTeams
assignments = {'match':matchNum, 'assignments':{}}
numScouts = len(scouts)
availableScouts = scouts
for team in teams:
	for x in range(numScouts/len(teams)):
		chosenScout = random.choice(availableScouts)
		assignments['assignments'].update({chosenScout:{'team':team,'alliance':('red' if team in redTeams else 'blue')}})
		availableScouts.remove(chosenScout)
extraTeams = random.sample(set(teams), numScouts%len(teams))
for team in extraTeams:
	chosenScout = random.choice(availableScouts)
	assignments['assignments'].update({chosenScout:{'team':team,'alliance':('red' if team in redTeams else 'blue')}})
	availableScouts.remove(chosenScout)
with open('../Documents/exampleAssignment.txt', 'w') as f:
	f.write(json.dumps(assignments))
#'''
# Main system
assignments = dict(db.child('scouts').get().val())
assignments['assignments'] = dict({k:v for k, v in assignments['assignments'].items() if assignments['assignments'][k]['team'] != -1})
#'''
print("")

matchNum = assignments['match']
print("Match: %s" % matchNum)
print("")
filename = "Q"+str(matchNum)+'.txt'

notsent = []
for device in devices:
	print("Sending to %s..." % device)
	service_matches = bluetooth.find_service(name=b'OBEX Object Push', address = devices[device] )
	if len(service_matches) == 0:
		print("[W] %s not found, not sent." % device)
		notsent.append(device)
	else:
		first_match = service_matches[0]
		port = first_match["port"]
		name = first_match["name"]
		host = first_match["host"]

		print("Connecting to \"%s\" on %s" % (name, host))
		client = Client(host, port)
		client.connect()
		client.put(filename, json.dumps(assignments))
		client.disconnect()
		print("Closed connection to %s." % device)

for x in range(15):
	if len(notsent) == 0:
		break
	else:
		for device in notsent:
			print("Sending to %s..." % device)
			service_matches = bluetooth.find_service(name=b'OBEX Object Push', address = devices[device] )
			print(service_matches)
			if len(service_matches) == 0:
				print("[W] %s not found, not sent." % device)
				notsent.append(device)
			else:
				first_match = service_matches[0]
				port = first_match["port"]
				name = first_match["name"]
				host = first_match["host"]

				print("Connecting to \"%s\" on %s" % (name, host))
				client = Client(host, port)
				client.connect()
				client.put(filename, json.dumps(assignments))
				client.disconnect()
				print("Closed connection to %s." % device)
