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

#url = 'servervartest-2018'
url = 'scouting-2018-9023a'

config = {
	'apiKey': 'mykey',
	'authDomain': url + '.firebaseapp.com',
	'databaseURL': 'https://' + url + '.firebaseio.com/',
	'storageBucket': url + '.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

devices = {
	'scout1': 'AC:22:0B:E3:1A:26',
	#'scout2': 'AC:22:0B:E3:14:AE',
	#'scout3': '14:DD:A9:47:40:80',
	#'scout4': '30:5A:3A:8E:D2:86',
	#'scout5': 'AC:22:0B:E3:16:84',
	#'scout6': 'AC:22:0B:E3:1E:FF',
	#'scout7': 'AC:63:BE:A8:28:29',s
	#'scout8': 'AC:63:BE:2D:DF:70',
	#'scout9': '84:D6:D0:13:46:8C',
	##'scout10': '84:D6:D0:E7:EE:26',
	##'scout11': '44:65:0D:06:02:BD',
	##'scout12': 'AC:63:BE:BD:87:10',
	##'scout13': '10:BF:48:E8:F7:6A',
	#'scout14': '30:85:A9:DD:97:9C',
	#'scout15': '30:85:A9:DC:1D:FC',
	#'scout16': '30:85:A9:DA:ED:98',
	#'scout17': '30:85:A9:DD:90:92',
	#'scout18': '30:85:A9:DF:D8:88'
	#'blue_super': 'AC:22:0B:5E:A2:41',
}

if resendMode == 1:
	devices = {k:v for k,v in devices.iteritems() if int(k[5:]) in resendIDs}

print(devices)


scouts = 'Nathan Justin Joey Noah Anoushka Zoe Rolland Teo Hanson Jack Tim Calvin Asha'
#scouts = 'Zach James Gemma Carl Freddy Carter Kenny Emily Eli Stephen Aidan Lyra Aakash Amanda'
scouts = scouts.split()


# Backup assignment system

with open(os.path.join(home, 'Documents/dallasIndex.json'), 'r') as f:
	matchIndex = json.load(f)
# Using for scout training until full system implemented
matchNum = db.child("currentMatchNum").get().val()
print("Match: %s" % matchNum)
filename = "Q"+str(matchNum)+'.txt'
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
'''
assignments = db.child('scouts').get().val()
assignments['assignments'] = {k for k in assignments['assignments'] if assignments['assignments'][k]['team'] != -1}
'''
print("")

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

while True:
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
