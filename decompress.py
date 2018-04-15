#!/usr/bin/python
import json
import sys
import pyrebase

url = 'scouting-2018-temp'

config = {
	'apiKey': 'mykey',
	'authDomain': url + '.firebaseapp.com',
	'databaseURL': 'https://' + url + '.firebaseio.com/',
	'storageBucket': url + '.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

compressKeys = {
	"C": "partnerLiftType",
	"B": "didPark",
	"E": "matchNumber",
	"D": "passiveClimb",
	"G": "climb",
	"F": "numCubesFumbledAuto",
	"I": "alliancePlatformIntakeTele",
	"H": "numElevatedPyramidIntakeAuto",
	"K": "didSucceed",
	"J": "layer",
	"M": "numGroundPortalIntakeTele",
	"L": "numExchangeInput",
	"Q": "activeLift",
	"P": "soloClimb",
	"S": "scaleAttemptTele",
	"$": "scaleAttemptAuto",
	"R": "numElevatedPyramidIntakeTele",
	"T": "didGetDisabled",
	"W": "allianceSwitchAttemptAuto",
	"V": "didMakeAutoRun",
	"Y": "numSpilledCubesAuto",
	"Z": "numSpilledCubesTele",
	"a": "endTime",
	"c": "numReturnIntake",
	"b": "teamNumber",
	"e": "scoutName",
	"g": "numGroundIntakeTele",
	"f": "startTime",
	"i": "numGroundPyramidIntakeAuto",
	"h": "allianceSwitchAttemptTele",
	"k": "assistedClimb",
	"j": "didFailToLift",
	"m": "startingPosition",
	"l": "opponentSwitchAttemptTele",
	"o": "alliancePlatformIntakeAuto",
	"n": "numGroundPyramidIntakeTele",
	"q": "numCubesFumbledTele",
	"p": "numHumanPortalIntakeTele",
	"r": "status",
	"t": "opponentPlatformIntakeTele",
	"w": "numRobotsLifted",
	"v": "didClimb",
	"y": "didGetIncapacitated",
	"z": "totalNumScaleFoul",
	"?": "time",
	"+": "vault",
	"<": "cubes",
	">": "cycleNumber",
	"!": "mode",
}

compressValues = {
	"A": "balanced",
	"O": "right",
	"N": "left",
	"s": "active",
	"U": "opponentOwned",
	"x": "passive",
	"X": "both",
	"u": "owned",
	"d": "center",
	"^": "assisted",
	"*": "QR",
	"(": "backup",
	")": "override",
}

boolsList = ['didMakeAutoRun', 'didFailToLift', 'didSucceed', 'didPark', 'didClimb', 'didGetDisabled', 'didGetIncapacitated']
listOfBoolsList = ['alliancePlatformIntakeAuto', 'alliancePlatformIntakeTele', 'opponentPlatformIntakeTele']

if len(sys.argv) == 2:
	data = str(sys.argv[1])

timdName = data.split("|")[0]
timdData = data.split("|")[1]

lastComma = -1
bracketLevel = 0
curlyBracketLevel = 0

firstDict = {}
for ix in range(len(timdData)):
	character = timdData[ix]
	if character == ':' and bracketLevel == 0 and curlyBracketLevel == 0:
		timdData = timdData[:ix] + '|' + timdData[ix+1:]
	if character == "{":
		curlyBracketLevel += 1
	elif character == "}":
		curlyBracketLevel += -1
	elif character == "[":
		bracketLevel += 1
	elif character == "]":
		bracketLevel += -1
	elif character == ",":
		if bracketLevel == 0 and curlyBracketLevel == 0:
			data = timdData[lastComma+1:ix]
			firstDict[compressKeys[data.split("|")[0]]] = data.split("|")[1]
			lastComma = ix
	if ix == len(timdData)-1:
		if bracketLevel == 0 and curlyBracketLevel == 0:
			data = timdData[lastComma+1:ix+1]
			firstDict[compressKeys[data.split("|")[0]]] = data.split("|")[1]

for k, v in firstDict.items():
	if k in boolsList:
		firstDict[k] = True if v == "1" else False
	elif v in compressValues:
		firstDict[k] = compressValues[v]
	elif v[0] == '[':
		lastComma = 0
		curlyBracketLevel = 0
		listData = []
		for ix in range(1, len(v)-1):
			character = v[ix]
			if character == "{":
				curlyBracketLevel += 1
			elif character == "}":
				curlyBracketLevel += -1
			elif character == ",":
				if curlyBracketLevel == 0:
					data = firstDict[k][lastComma+1:ix]
					listData.append(data)
					lastComma = ix
			if ix == len(v)-2:
				if curlyBracketLevel == 0:
					data = firstDict[k][lastComma+1:ix+1]
					listData.append(data)
		firstDict[k] = listData

	elif v[0] == '{': # Untested code, be wary
		lastComma = -1
		bracketLevel = 0
		curlyBracketLevel = 0
		for ix in range(len(v)):
			character = v[ix]
			if character == ':' and bracketLevel == 0 and curlyBracketLevel == 0:
				firstDict[k] = firstDict[k][:ix] + '|' + firstDict[k][ix+1:]
			if character == "{":
				curlyBracketLevel += 1
			elif character == "}":
				curlyBracketLevel += -1
			elif character == "[":
				bracketLevel += 1
			elif character == "]":
				bracketLevel += -1
			elif character == ",":
				if bracketLevel == 0 and curlyBracketLevel == 0:
					data = firstDict[k][lastComma+1:ix]
					firstDict[k][compressKeys[data.split("|")[0]]] = data.split("|")[1]
					lastComma = ix
			if ix == len(v)-1:
				if bracketLevel == 0 and curlyBracketLevel == 0:
					data = firstDict[k][lastComma+1:ix+1]
					firstDict[k][compressKeys[data.split("|")[0]]] = data.split("|")[1]
	else:
		try:
			int(v)
		except:
			try:
				float(v)
			except:
				pass
			else:
				firstDict[k] = float(v)
		else:
			firstDict[k] = int(v)

print("")
# Iterates through the lists
for k,v in firstDict.items():
	if k in listOfBoolsList:
		firstDict[k] = [True if v2 == '1' else False for v2 in v]
	elif type(v) == list:
		for ix in range(len(v)):
			v2 = v[ix]
			if v2[0] == '{':
				lastComma = 0
				curlyBracketLevel = 0
				updateDict = {}
				for ix2 in range(1, len(v2)-1):
					character = v2[ix2]
					if character == ':' and curlyBracketLevel == 0:
						firstDict[k][ix] = firstDict[k][ix][:ix2] + '|' + firstDict[k][ix][ix2+1:]
					if character == "{":
						curlyBracketLevel += 1
					elif character == "}":
						curlyBracketLevel += -1
					elif character == "[":
						bracketLevel += 1
					elif character == "]":
						bracketLevel += -1
					elif character == ",":
						if bracketLevel == 0 and curlyBracketLevel == 0:
							data = firstDict[k][ix][lastComma+1:ix2]
							updateDict[compressKeys[data.split("|")[0]]] = data.split("|")[1]
							lastComma = ix2
					if ix2 == len(v2)-2:
						if bracketLevel == 0 and curlyBracketLevel == 0:
							data = firstDict[k][ix][lastComma+1:ix2+1]
							updateDict[compressKeys[data.split("|")[0]]] = data.split("|")[1]
				if updateDict != {}:
					firstDict[k][ix] = updateDict

				for k3, v3 in firstDict[k][ix].items():
					if v3[0] == '{':
						lastComma = 0
						curlyBracketLevel = 0
						updateDict = {}
						for ix3 in range(1, len(v3)-1):
							character = v3[ix3]
							if character == ':' and curlyBracketLevel == 0:
								firstDict[k][ix][k3] = firstDict[k][ix][k3][:ix3] + '|' + firstDict[k][ix][k3][ix3+1:]
							if character == "{":
								curlyBracketLevel += 1
							elif character == "}":
								curlyBracketLevel += -1
							elif character == "[":
								bracketLevel += 1
							elif character == "]":
								bracketLevel += -1
							elif character == ",":
								if bracketLevel == 0 and curlyBracketLevel == 0:
									data = firstDict[k][ix][k3][lastComma+1:ix3]
									updateDict[compressKeys[data.split("|")[0]]] = data.split("|")[1]
									lastComma = ix3
							if ix3 == len(v3)-2:
								if bracketLevel == 0 and curlyBracketLevel == 0:
									data = firstDict[k][ix][k3][lastComma+1:ix3+1]
									updateDict[compressKeys[data.split("|")[0]]] = data.split("|")[1]

						if updateDict != {}:
							firstDict[k][ix][k3] = updateDict
						for k4, v4 in firstDict[k][ix][k3].items():
							if k4 in compressKeys:
								k4 = compressKeys[k4]
							if k4 in boolsList:
								v4 = True if v4 == '1' else False
							elif v4 in compressValues:
								v4 = compressValues[v4]
							else:
								try:
									int(v4)
								except:
									try:
										float(v4)
									except:
										pass
									else:
										v4 = float(v4)
								else:
									v4 = int(v4)
							firstDict[k][ix][k3][k4] = v4

					elif v3 in compressValues:
						firstDict[k][ix][k3] = compressValues[v3]
					elif k3 in boolsList:
						firstDict[k][ix][k3] = True if v3 == "1" else False
					else:
						try:
							int(v3)
						except:
							try:
								float(v3)
							except:
								pass
							else:
								firstDict[k][ix][k3] = float(v3)
						else:
							firstDict[k][ix][k3] = int(v3)

			else:
				print("Error: needs more continuation")

if "-" in timdName and "Q" in timdName:
	try:
		int(timdName.split("-")[1])
		int(timdName.split("Q")[0])
		int(timdName.split("Q")[1].split("-")[0])
	except:
		pass
	else:
		db.child("TempTeamInMatchDatas/"+str(timdName)).set(firstDict)

print("Done.")
