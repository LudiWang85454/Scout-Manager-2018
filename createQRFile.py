import bluetooth
from PyOBEX.client import Client
import pyrebase
import requests
import os
import json
import random

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

def makeASCIIFromJSON(input):
	if isinstance(input, dict):
		return dict((makeASCIIFromJSON(k), makeASCIIFromJSON(v)) for k, v in input.items())
	elif isinstance(input, list):
		return map(lambda i: makeASCIIFromJSON(i), input)
	elif isinstance(input, str):
		return input.encode('utf-8')
	else:
		return input

print("Pulling data from firebase...")
key = "2018" + str(db.child("TBAcode").get().val())
base_url = "https://www.thebluealliance.com/api/v3/"
headerkey = "X-TBA-Auth-Key"
with open(os.path.join(home, 'Downloads/data/TBAapikey.txt'), 'r') as f:
	authcode = f.read()

eventKeyRequestURL = base_url + "event/"+key+"/matches/simple"

print("Pulling data from TBA...")
matchData = requests.get(eventKeyRequestURL, headers = {headerkey: authcode}).json() 
matchData = makeASCIIFromJSON(matchData)

if type(matchData) == dict:
	print("Error getting data from TBA, check 'TBACode' on firebase! ")

matchIndex = {match['match_number']:matchData.index(match) for match in matchData if match['comp_level']=='qm'}

# Creates letter assignements
scouts = "Aakash Aidan Amanda Asha Calvin Carl Carter David Emily Erik Freddy Hanson Jack James Joey Justin Kenny Lasthenia Nathan Sam Stephen Teo Tim Zachary Zatara Zoe".split()

letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
fullLetters = {}
for scout in scouts:
	choice = random.choice(letters)
	fullLetters[scout] = choice
	letters.remove(choice)

fullAssignments = {}
for match in matchIndex:
	index = matchIndex[match]
	matchNum = matchData[index]['match_number']
	redTeams = matchData[index]['alliances']['red']['team_keys']
	redTeams = [int(team[3:]) for team in redTeams]
	blueTeams = matchData[index]['alliances']['blue']['team_keys']
	blueTeams = [int(team[3:]) for team in blueTeams]
	teams = redTeams + blueTeams
	assignments = {}
	numScouts = 18
	scoutSPRRankings = [[1,2,3,4,5,6],[7,8,9,10,11,12],[13,14,15,16,17,18]]
	# Required list() to prevent availableScouts from being linked to scoutSPRRankings, which causes removed scouts to not be returned
	availableScouts = list(scoutSPRRankings)
	for team in teams:
		for x in range(numScouts/len(teams)):
			chosenScout = random.choice(availableScouts[x])
			assignments[chosenScout] = {'team':team, 'alliance':('red' if team in redTeams else 'blue')}
			availableScouts[x].remove(chosenScout)
	extraTeams = random.sample(set(teams), numScouts%len(teams))
	if len(availableScouts) != 0:
		availableScouts = [y for y in availableScouts for x in y]
	for team in extraTeams:
		chosenScout = random.choice(availableScouts)
		assignments.update({chosenScout:{'team':team,'alliance':('red' if team in redTeams else 'blue')}})
		availableScouts.remove(chosenScout)
	fullAssignments["match"+str(matchNum)] = assignments

data = {"matches":fullAssignments,"letters":fullLetters}

with open(os.path.join(home, 'Downloads/data/QRAssignments.json'), 'w') as f:
	json.dump(data, f)

with open(os.path.join(home, 'Downloads/data/QRAssignments.txt'), 'w') as f:
	f.write(json.dumps(data))

with open(os.path.join(home, 'Downloads/data/activeScouts.json'), 'r') as f:
	devices = json.load(f)

while True:
	x = raw_input("Would you like to send (y/n): ")
	if x in ["y", "Y"]:
		os.system("python " +os.path.join(home, 'scoutManager/sendQRFile.py'))
		break
	elif x in ["n", "N"]:
		break