import bluetooth
from PyOBEX.client import Client
import pyrebase
import requests
import os
import json
import random

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

scouts = [str(x) for x in db.child('scouts/assignments').get().val()]

def makeASCIIFromJSON(input):
	if isinstance(input, dict):
		return dict((makeASCIIFromJSON(k), makeASCIIFromJSON(v)) for k, v in input.items())
	elif isinstance(input, list):
		return map(lambda i: makeASCIIFromJSON(i), input)
	elif isinstance(input, str):
		return input.encode('utf-8')
	else:
		return input

key = "2018" + str(db.child("TBAcode").get().val())
base_url = "https://www.thebluealliance.com/api/v3/"
headerkey = "X-TBA-Auth-Key"
with open(os.path.join(home, 'Downloads/data/TBAapikey.txt'), 'r') as f:
	authcode = f.read()

eventKeyRequestURL = base_url + "event/"+key+"/matches/simple"

matchData = requests.get(eventKeyRequestURL, headers = {headerkey: authcode}).json() 
matchData = makeASCIIFromJSON(matchData)

matchIndex = {match['match_number']:matchData.index(match) for match in matchData if match['comp_level']=='qm'}

fullAssignments = {}
for match in matchIndex:
	index = matchIndex[match]
	matchNum = matchData[index]['match_number']
	redTeams = matchData[index]['alliances']['red']['team_keys']
	redTeams = [int(team[3:]) for team in redTeams]
	blueTeams = matchData[index]['alliances']['blue']['team_keys']
	blueTeams = [int(team[3:]) for team in blueTeams]
	teams = redTeams + blueTeams
	assignments = {'match':matchNum, 'assignments':{}}
	numScouts = len(scouts)
	# Required list() to prevent availableScouts from being linked to scouts, which causes removed scouts to not be returned
	availableScouts = list(scouts)
	for team in teams:
		for x in range(numScouts/len(teams)):
			chosenScout = random.choice(availableScouts)
			assignments['assignments'][chosenScout] = {'team':team, 'alliacne':('red' if team in redTeams else 'blue')}
			availableScouts.remove(chosenScout)
	extraTeams = random.sample(set(teams), numScouts%len(teams))
	for team in extraTeams:
		chosenScout = random.choice(availableScouts)
		assignments['assignments'].update({chosenScout:{'team':team,'alliance':('red' if team in redTeams else 'blue')}})
		availableScouts.remove(chosenScout)
	fullAssignments[str(matchNum)] = assignments

with open(os.path.join(home, 'Downloads/data/backupAssignments.json'), 'w') as f:
	json.dump(fullAssignments, f)

with open(os.path.join(home, 'Downloads/data/backupAssignments.txt'), 'w') as f:
	f.write(json.dumps(fullAssignments))

with open(os.path.join(home, 'Downloads/data/activeScouts.json'), 'r') as f:
	devices = json.load(f)

filename = 'backupAssignments.txt'
dataToSend = json.dumps(fullAssignments)

notSent = []
for device in devices:
	print("Sending to %s..." % device)
	service_matches = bluetooth.find_service(name=b'OBEX Object Push', address = devices[device] )
	print(service_matches)
	if len(service_matches) == 0:
	    print("[W] %s not found, not sent." % device)
	    notSend.append(device)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print("Connecting to \"%s\" on %s" % (name, host))
	client = Client(host, port)
	client.connect()
	client.put(filename, dataToSend)
	client.disconnect()
	print("Successfuly sent to %s." % device)

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
				client.put(filename, dataToSend)
				client.disconnect()
				print("Closed connection to %s." % device)
