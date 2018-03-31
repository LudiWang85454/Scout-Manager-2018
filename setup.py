import json
import os

home = os.path.expanduser('~')
apikey = raw_input("Please enter your slack API key or press 'enter' to skip: ")

data = {
	'scout1': 'AC:22:0B:E3:1A:26',
	'scout2': 'AC:22:0B:E3:14:AE',
	'scout3': '14:DD:A9:47:40:80',
	'scout4': '30:5A:3A:8E:D2:86',
	'scout5': 'AC:22:0B:E3:16:84',
	'scout6': 'AC:22:0B:E3:1E:FF',
	'scout7': 'AC:63:BE:A8:28:29',
	'scout8': 'AC:63:BE:2D:DF:70',
	'scout9': '84:D6:D0:13:46:8C',
	'scout10': '84:D6:D0:E7:EE:26',
	'scout11': '44:65:0D:06:02:BD',
	'scout12': 'AC:63:BE:BD:87:10',
	'scout13': '10:BF:48:E8:F7:6A',
	'scout14': '30:85:A9:DD:97:9C',
	'scout15': '30:85:A9:DC:1D:FC',
	'scout16': '30:85:A9:DA:ED:98',
	'scout17': '30:85:A9:DD:90:92',
	'scout18': '30:85:A9:DF:D8:88'
}

print("\nIs this laptop for (A) scouts 1-9 or (B) scouts 10-18?")

while True:
	x = raw_input("Please enter A or B: ")
	if x in ['a', 'A']:
		data = {k:v for k, v in data.items() if int(k[5:]) in range(1,10)}
		break
	elif x in ['b', 'B']:
		data = {k:v for k, v in data.items() if int(k[5:]) in range(10,19)}
		break

if not os.path.exists(os.path.join(home, 'Downloads/data')):
	os.makedirs(os.path.join(home, 'Downloads/data'))
if not os.path.exists(os.path.join(home, 'Downloads/sent')):
	os.makedirs(os.path.join(home, 'Downloads/sent'))

with open(os.path.join(home, 'Downloads/data/activeScouts.json'), 'w') as f:
	json.dump(data, f)

with open(os.path.join(home, 'Downloads/data/activeScoutsBackup.json'), 'w') as f:
	json.dump(data, f)

if apikey != "":
	with open(os.path.join(home, 'Downloads/data/apikey.txt'), 'w') as f:
		f.write(apikey)

with open(os.path.join(home, 'Downloads/data/lastSentMatch.txt'), 'w') as f:
	f.write("0")

with open(os.path.join(home, 'Downloads/data/lastSentAssignment.txt'), 'w') as f:
	f.write("0")

with open(os.path.join(home, 'Downloads/data/lastSentCycle.txt'), 'w') as f:
	f.write("0")

with open(os.path.join(home, 'scoutManager/databaseListener.service'), 'w') as f:
	f.write('''[Unit]
Description=Simplified firebase listener
After=syslog.target

[Service]
Type=simple
User=%s
WorkingDirectory=%s/scoutManager
ExecStart=/usr/bin/python %s/scoutManager/databaseListener.py
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
		''' % (home[6:], home, home))

with open(os.path.join(home, 'scoutManager/scheduler.service'), 'w') as f:
	f.write('''[Unit]
Description=Simplified python script scheduler
After=syslog.target

[Service]
Type=simple
User=%s
WorkingDirectory=%s/scoutManager
ExecStart=/usr/bin/python %s/scoutManager/scheduler.py
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
		''' % (home[6:], home, home))

os.system("sudo cp "+os.path.join(home, "scoutManager/databaseListener.service")+" /etc/systemd/system/databaseListener.service")
os.system("sudo cp "+os.path.join(home, "scoutManager/scheduler.service")+" /etc/systemd/system/scheduler.service")
os.remove(os.path.join(home, 'scoutManager/databaseListener.service'))
os.remove(os.path.join(home, 'scoutManager/scheduler.service'))
os.system("sudo chmod +x /etc/systemd/system/databaseListener.service")
os.system("sudo chmod +x /etc/systemd/system/scheduler.service")
os.system("sudo chmod +x "+os.path.join(home, 'scoutManager/scoutNotSent.py'))
os.system("sudo chmod +x "+os.path.join(home, 'scoutManager/searchFolder.py'))
os.system("sudo chmod +x "+os.path.join(home, 'scoutManager/sendSlackNotifications.py'))
os.system("sudo chmod +x "+os.path.join(home, 'scoutManager/updateQRCode.py'))
os.system("sudo chmod +x "+os.path.join(home, 'scoutManager/decompress.py'))
os.system("sudo chmod +x "+os.path.join(home, 'scoutManager/decompressScheduler.py'))
os.system("sudo systemctl daemon-reload")
os.system("sudo systemctl enable databaseListener.service")
os.system("sudo systemctl enable scheduler.service")
os.system("sudo systemctl start databaseListener.service")
os.system("sudo systemctl start scheduler.service")

print("Done.")

print("Please run the following commands:\nsystemctl status databaseListener\nsystemctl status scheduler\n\nIf these both are good, you're done!")