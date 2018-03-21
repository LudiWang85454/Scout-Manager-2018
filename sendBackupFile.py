import bluetooth
from PyOBEX.client import Client
import pyrebase
import requests
import os
import json
import random

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

scouts = [str(x) for x in db.child('scouts/assignments').get().val()]
print(scouts)

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
print(key)
base_url = "https://www.thebluealliance.com/api/v3/"
headerkey = "X-TBA-Auth-Key"
with open(os.path.join(home, 'Downloads/data/TBAapikey.txt'), 'r') as f:
	headervalue = f.read()

eventKeyRequestURL = base_url + "event/"+key+"/matches/simple"#'event/' + key + "/teams" #"_" + match

matchData = requests.get(eventKeyRequestURL, headers = {headerkey: headervalue}).json() 
matchData = makeASCIIFromJSON(matchData)

with open('test.txt', 'w') as f:
	json.dump(matchData, f)

matchIndex = {match['match_number']:matchData.index(match) for match in matchData if match['comp_level']=='qm'}
print(matchIndex)

fullAssignments = {}
for match in matchIndex:
	index = matchIndex[match]
	matchNum = matchData[index]['match_number']
	print(matchNum, index)
	redTeams = matchData[index]['alliances']['red']['team_keys']
	redTeams = [int(team[3:]) for team in redTeams]
	blueTeams = matchData[index]['alliances']['blue']['team_keys']
	blueTeams = [int(team[3:]) for team in blueTeams]
	teams = redTeams + blueTeams
	print(teams)
	assignments = {'match':matchNum, 'assignments':{}}
	numScouts = len(scouts)
	availableScouts = scouts
	for team in teams:
		for x in range(numScouts/len(teams)):
			chosenScout = random.choice(availableScouts)
			assignments['assignments'].update({chosenScout:{'team':team,'alliance':('red' if team in redTeams else 'blue')}})
			availableScouts.remove(chosenScout)
			print('1', assignments)
	extraTeams = random.sample(set(teams), numScouts%len(teams))
	for team in extraTeams:
		chosenScout = random.choice(availableScouts)
		assignments['assignments'].update({chosenScout:{'team':team,'alliance':('red' if team in redTeams else 'blue')}})
		availableScouts.remove(chosenScout)
	print('t', assignments)
	fullAssignments[str(matchNum)] = assignments

print(fullAssignments)

with open(os.path.join(home, 'Downloads/data/activeScouts.json'), 'r') as f:
	devices = json.load(f)

for device in devices:
	print("Sending to %s..." % device)
	service_matches = bluetooth.find_service(name=b'OBEX Object Push', address = devices[device] )
	print(service_matches)
	if len(service_matches) == 0:
	    print("[W] %s not found, not sent." % device)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print("Connecting to \"%s\" on %s" % (name, host))
	client = Client(host, port)
	client.connect()
	client.put("backupFile.txt", "Hello world\n")
	client.disconnect()
	print("Successfuly sent to %s." % device)
