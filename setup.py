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

with open(os.path.join(home, 'Downloads/data/activeScouts.json'), 'w') as f:
	json.dump(data, f)

with open(os.path.join(home, 'Downloads/data/activeScoutsBackup.json'), 'w') as f:
	json.dump(data, f)

with open(os.path.join(home, 'Downloads/data/apikey.txt'), 'w') as f:
	f.write(apikey)

with open(os.path.join(home, 'Downloads/data/lastMatch.txt'), 'w') as f:
	f.write("0")

print("Done.")
print("Please modify activeScouts.json and comment out the scouts that are not used on this computer.")