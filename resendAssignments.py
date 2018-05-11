import os

scoutNums = []

def getInput():
	global scoutNums
	num = raw_input('Enter scout number or "d" if done: ')
	if num == 'd':
		return
	else:
		try:
			int(num)
			scoutNums.append(num)
		except ValueError:
			print("Please enter an integer.")
		return getInput()

getInput()

scoutStr = ""
for x in scoutNums:
	scoutStr += str(x)


os.system("python sendAssignments.py resend "+scoutStr)
