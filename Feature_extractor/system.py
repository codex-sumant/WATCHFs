import subprocess
import os
import re

def feature_extractor():
	PATH='/home/sumant/WATCHFs/files/newlogfile.txt'

	subprocess.call('rm /home/sumant/WATCHFs/files/results.csv', shell=True)

	elfs = open(PATH, 'r')
	paths=elfs.readlines()

	for file in paths:
		file.splitlines()[0]
		print(file)
		subprocess.call("python /home/sumant/WATCHFs/Feature_extractor/ELFMiner.py "  + file , shell=True)


