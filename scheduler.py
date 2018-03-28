#!/usr/bin/python -p
import subprocess
import os
import time

home = os.path.expanduser('~')

while True:
	subprocess.call(os.path.join(home, 'Desktop/searchFolder.py'))
	time.sleep(30)