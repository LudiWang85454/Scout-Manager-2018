#!/usr/bin/python -p
import subprocess
import os
import time

home = os.path.expanduser('~')

while True:
	subprocess.call(os.path.join(home, 'scoutManager/decompressScheduler.py'))
	time.sleep(15)
	subprocess.call(os.path.join(home, 'scoutManager/decompressScheduler.py'))
	subprocess.call(os.path.join(home, 'scoutManager/searchFolder.py'))
	time.sleep(15)