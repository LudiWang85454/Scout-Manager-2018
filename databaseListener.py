#!/usr/bin/python -p
import os
import pyrebase
import subprocess

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

def stream_assignment_handler(message):
	if type(message["data"]) == int:
		with open(os.path.join(home, 'Downloads/data/lastSentAssignment.txt'), 'r') as f:
			cycle = f.read()
		if cycle == "":
			cycle = 0
		if message["data"] != int(cycle):
			subprocess.call(os.path.join(home, "scoutManager/sendAssignments.py"), shell=True)
			with open(os.path.join(home, 'Downloads/data/lastSentAssignment.txt'), 'w') as f:
				f.write(str(message["data"]))

def stream_match_handler(message):
	if type(message["data"]) == int:
		with open(os.path.join(home, 'Downloads/data/lastSentMatch.txt'), 'r') as f:
			cycle = f.read()
		if cycle == "":
			cycle = 0
		if message["data"] != int(cycle) and home == "/home/citrus": # Prevents double slack notification
			if message["data"] > 2:
				subprocess.call("python3 " +os.path.join(home, "scoutManager/scoutNotSent.py"), shell=True)
			with open(os.path.join(home, 'Downloads/data/lastSentMatch.txt'), 'w') as f:
				f.write(str(message["data"]))


def stream_cycle_handler(message):
	if type(message["data"]) == int:
		with open(os.path.join(home, 'Downloads/data/lastSentCycle.txt'), 'r') as f:
			cycle = f.read()
		if cycle == "":
			cycle = 0
		if message["data"] != int(cycle):
			subprocess.call(os.path.join(home, "scoutManager/updateQRCode.py"), shell=True)
			with open(os.path.join(home, 'Downloads/data/lastSentCycle.txt'), 'w') as f:
				f.write(str(message["data"]))

#stream1 = db.child("scouts/cycle").stream(stream_assignment_handler)
stream3 = db.child("currentMatchNum").stream(stream_match_handler)
stream2 = db.child("cycleCounter").stream(stream_cycle_handler)
