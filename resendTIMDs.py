import os

matchNums = []

def getInput():
	global matchNums
	num = raw_input('Enter match number or "d" if done: ')
	if num == 'd':
		return
	else:
		try:
			int(num)
			matchNums.append(num)
		except ValueError:
			print("Please enter an integer.")
		return getInput()

getInput()
print("")

home = os.path.expanduser('~')
path = os.path.join(home, 'Downloads')

for file in os.listdir(os.path.join(path, 'sent')):
	# Checks if file is a .jsontxt file
    if file.endswith(".jsontxt"):
    	match = file.split('Q')[1].split('-')[0]
    	if match in matchNums:
    		print("Resent " + str(file))
    		os.rename(os.path.join(path, 'sent', file), os.path.join(path, file))

print("Done.")
