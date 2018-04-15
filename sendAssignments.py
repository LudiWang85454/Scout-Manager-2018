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

url = 'scouting-2018-temp'

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

# Main system
print("Pulling data from firebase...")
assignments = dict(db.child('scouts').get().val())
print("Done pulling data.")
assignments['matches'] = dict(assignments['matches'])
for matchdict in assignments['matches'].keys():
	assignments['matches'][matchdict] == dict(assignments['matches'][matchdict])
	for k,v in assignments['matches'][matchdict].items():
		if assignments['matches'][matchdict][k]['team'] == -1:
			assignments['matches'][matchdict].pop(k)
		else:
			assignments['matches'][matchdict][k] == dict(assignments['matches'][matchdict][k])

print("")

cycleNum = assignments['cycle']
print("Match: %s" % cycleNum)
print("")
filename = "C"+str(cycleNum)+'.txt'

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
		client.put(filename, json.dumps(assignments['matches']))
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
				client.put(filename, json.dumps(assignments['matches']))
				client.disconnect()
				print("Closed connection to %s." % device)
