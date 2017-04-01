import sys
import re
import json
# Import the os module, for the os.walk function
import os

# This script was for cleaning up a bunch of files that had timestamps in them
# For Quantified Self Portrait

# Set the directory you want to start from
rootDir = 'json/stamps'

#for dirName, subdirList, fileList in os.walk(rootDir):
for root, dirs, files in os.walk(rootDir):
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']
    # use files and dirs
    print('Found directory: %s' % dirs)
    for fname in files:
#		my_mbox = open(filetest)
		my_mbox = open(rootDir + '/' + fname)
		instamps = 'cleanedINstamps.txt'
		outstamps = 'cleanedOUTstamps.txt'
		logfile = 'cleanedLogfile.txt'
		i = open(instamps, 'w')
		o = open(outstamps, 'w')
		l = open(logfile, 'w')

		inMatch = re.search(r'INstamps', fname)
		outMatch = re.search(r'OUTstamps', fname)
		if (inMatch):
			print('\t IN %s' % fname)
			for line in my_mbox:
#				print(line)

				earlyMatch = re.search(r'2017', line)
				lateMatch = re.search(r'2015', line)
#				print(line)
				if (earlyMatch):
					l.write(line)
					continue
				elif (lateMatch):
					l.write(line)
					break
				else:
					i.write(line)
'''
		elif (outMatch):
			o.write(line)

			print('\t OUT %s' % fname)
'''		
i.close()
o.close()
l.close()

