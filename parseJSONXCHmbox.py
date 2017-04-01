import sys
import re
import json
# Import the os module, for the os.walk function
import os
 
# Set the directory you want to start from
rootDir = 'json'
box = 'CSIout'
newfile = 'CSI.OUT'
#for dirName, subdirList, fileList in os.walk(rootDir):
my_mbox = open('json/' + box + '.mbox.json')
instamps = 'json/stamps/'  + newfile + 'stamps.txt'
#outstamps = 'json/stamps/'  + box + 'stamps.txt'
logfile = 'json/stamps/'  + box + 'logfile.txt'
i = open(instamps, 'w')
#o = open(outstamps, 'w')
l = open(logfile, 'w')

for line in my_mbox:
#	print(line)
	parsed_json = json.loads(line)
	try:
		i.write(parsed_json['Date']  + '\n')
	except:
		print(line)
		pass
i.close()
#o.close()
l.close()

