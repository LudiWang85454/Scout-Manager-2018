#!/usr/bin/python
import pyrebase
import json
import os

home = os.path.expanduser('~')

url = 'scouting-2018-houston'

config = {
	'apiKey': 'mykey',
	'authDomain': url + '.firebaseapp.com',
	'databaseURL': 'https://' + url + '.firebaseio.com/',
	'storageBucket': url + '.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

QRurl = 'server-2018-3209b'

QRconfig = {
	'apiKey': 'mykey',
	'authDomain': QRurl + '.firebaseapp.com',
	'databaseURL': 'https://' + QRurl + '.firebaseio.com/',
	'storageBucket': QRurl + '.appspot.com'
}

QRfirebase = pyrebase.initialize_app(QRconfig)
QRdb = QRfirebase.database()

with open(os.path.join(home, 'Downloads/data/QRAssignments.json'), 'r') as f:
	data = json.load(f)

letters = data['letters']

print("Pulling data from firebase...")
availableScouts = [scout for scout, val in db.child('availability').get().val().items() if val == 1]
cycleNum = db.child('cycleCounter').get().val()
sprs = QRdb.child("SPRs").get().val()
print("Done pulling data.")
sprsAll = {scout:sprs[scout] if scout in sprs else 0 for scout in availableScouts}
availableSPRs = {scout:spr for scout, spr in sprsAll.items() if scout in availableScouts}

sortedSPRs = sorted(availableSPRs.items(), key=lambda x: x[1])
scouts = [x[0] for x in sortedSPRs]

qrstring = str(cycleNum)+'|' if cycleNum >= 10 else '0'+str(cycleNum)+'|'

for scout in scouts:
	qrstring += letters[scout]
print('Code: %s' % qrstring)
print("Sending to firebase...")
db.child('QRCode').set(qrstring)
print("")
print("Done.")
