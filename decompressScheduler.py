#!/usr/bin/python
import pyrebase
import subprocess
import os

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

data = db.child("TempQRTeamInMatchDatas").get().val()

if data != None:
	for key, value in data.items():
		subprocess.call("python "+os.path.join(home, "scoutManager/decompress.py")+' "'+str(value)+'"', shell=True)
		db.child("TempQRTeamInMatchDatas/"+str(key)).remove()