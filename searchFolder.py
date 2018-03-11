import os
import json

path = '/home/sam/Downloads'

for file in os.listdir(path):
    if file.endswith(".txt"):
    	print(file.split('.')[0])
       	fullPath = os.path.join(path, file)
        with open(fullPath, 'r') as f:
        	data = json.load(f)
        	print(data)