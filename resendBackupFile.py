import bluetooth
from PyOBEX.client import Client
import os
import json

home = os.path.expanduser('~')

# Input (don't edit manually in script, run it)
resendIDs = []
resendMode = 1

def getInput():
	global resendIDs
	num = raw_input('Enter scout number, "a" to resend all, or "d" if done: ')
	if num == 'd':
		return
	elif num == 'a':
		global resendMode
		resendMode = 0
	else:
		try:
			int(num)
			resendIDs.append(num)
		except ValueError:
			print("Please enter an integer.")
		return getInput()

getInput()

if resendMode == 1:
	devices = {k:v for k,v in devices.iteritems() if int(k[5:]) in resendIDs}

with open(os.path.join(home, 'Downloads/data/backupAssignments.json'), 'r') as f:
	fullAssignments = json.load(f)

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