import sys
import re
import json
import csv
# Import the os module, for the os.walk function
import os

#This script reads a JSONified mbox file, and writes selected values to a CSV
#right now it is set up to output a list of all email addresses that appear in the
#"To" field in sent message (e.g. Everyone I have ever emailed)
#It also adds some category info based of some simple regex keyword searches

#import for parsing email address
from email.utils import parseaddr

# reads parsed JSON and makes in/out timestamp lists.

# Set the directory you want to start from
rootDir = 'parsing-contacts'
outputDir = rootDir + '/output'
filetest = 'nyap.mbox.json'

if not os.path.exists(outputDir):
	os.makedirs(outputDir)



# Set message attribute name you want to look for
inKey = 'Subject'
outKey = 'Date'
category =''

findTo = True

#for dirName, subdirList, fileList in os.walk(rootDir):
for root, dirs, files in os.walk(rootDir):
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']
    # use files and dirs
    print('Found directory: %s' % dirs)
    for fname in files:
		print('\t%s' % fname)
		if len(dirs) > 0:
			del dirs[0]

#		my_mbox = open(rootDir + '/' + filetest)
		my_mbox = open(rootDir + '/' + fname)
		instamps = outputDir + '/' +  fname + '.INparsed.txt'
		outstamps = outputDir + '/' +  fname + '.OUTparsed.txt'
		logfile = outputDir + '/' + 'logfile.txt'
		output = open(outputDir + '/' +  fname + 'output.csv', 'wt')
		writer = csv.writer(output)
		i = open(instamps, 'w')
		o = open(outstamps, 'w')
		l = open(logfile, 'w')

		for line in my_mbox:
		#	print(line)
			parsed_json = json.loads(line)
			
            #Assign categories by keywords found in the email header or message
			afMatch1 = re.search(r'info@artandfeminism.org', line, re.IGNORECASE)
			afMatch2 = re.search(r'info@art.plusfeminism.org', line, re.IGNORECASE)
			afMatch3 = re.search(r'artandfeminism-organize', line, re.IGNORECASE)
			afMatch4 = re.search(r'artandfeminismwiki@gmail.com', line, re.IGNORECASE)
			wmnyc1 = re.search(r'wmnyc', line, re.IGNORECASE)
			wmnyc2 = re.search(r'wikimedia new york city', line, re.IGNORECASE)
			wmnyc3 = re.search(r'wikimedia nyc', line, re.IGNORECASE)
			wmnyc4 = re.search(r'babycastles', line, re.IGNORECASE)
			nyapMatch1 = re.search(r'info@artspracticum.org', line, re.IGNORECASE)
			nyapMatch2 = re.search(r'michael@artspracticum.org', line, re.IGNORECASE)
			cunyMatch1 = re.search(r'gc.cuny.edu', line, re.IGNORECASE)
			cunyMatch2 = re.search(r'csi.cuny.edu', line, re.IGNORECASE)
			cunyMatch3 = re.search(r'csimediaculture.com', line, re.IGNORECASE)
			nycc = re.search(r'nycc', line, re.IGNORECASE)
			nycc2 = re.search(r'\bsig\b', line, re.IGNORECASE)
			nycc3 = re.search(r'a-sig-classic-participants', line, re.IGNORECASE)
			googlegroup = re.search(r'googlegroups.com', line, re.IGNORECASE)		
			st1 = re.search(r'social text', line, re.IGNORECASE)
			st2 = re.search(r'socialtext', line, re.IGNORECASE)
			eyebeam = re.search(r'eyebeam', line, re.IGNORECASE)
			del1 = re.search(r'reply.craigslist.org', line, re.IGNORECASE)
			del2 = re.search(r'fhands', line, re.IGNORECASE)
			del3 = re.search(r'Payment received from', line, re.IGNORECASE)
			
			
			if (afMatch1 or afMatch2 or afMatch3 or afMatch3):
				category="af"
			elif (nyapMatch1 or nyapMatch2):
				category="nyap"
			elif (cunyMatch1 or cunyMatch2 or cunyMatch3):
				category="cuny"
			elif (nycc or nycc2 or nycc3):
				category="nycc"
			elif (st1 or st2):
				category="st"
			elif (eyebeam):
				category="eyebeam"
			elif (wmnyc1 or wmnyc2 or wmnyc3 or wmnyc4):
				category="eyebeam"
			elif (googlegroup):
				category="lists"
			elif (del1 or del2 or del3):
				category="delete"
			else:
				category=""
			
			
#			if (yearMatch):
#				l.write(line  + '\n\n')
	
#				break


            # This is checking the Inbox
			if 'X-Received' in parsed_json.keys(): #IN
				try:
#					print('in')
					i.write('\n')

#					i.write(parsed_json[inKey]  + '\n')

#					print(parsed_json['Delivered-To']) # only incoming emails have this field
#					if parsed_json['From'] == 'Michael Mandiberg <michael@mandiberg.com>':
#						l.write(parsed_json['From'] + '--------->>>>' + parsed_json['Delivered-To']  + '\n\n')
				except:
					l.write(line  + '\n\n')
	
					pass    
            # This is checking the Outbox
			elif 'Delivered-To' in parsed_json.keys():  #OUT
				try:
#					print(parsed_json['Delivered-To']) # only incoming emails have this field
					try:
#						print('outbound\n')

						for element in parsed_json['To']:
							nameEmailMatch = re.search(r"([A-Z]\w+)([A-Z]\w+)\"?\<?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", element) 
							print(nameEmailMatch.group(1),nameEmailMatch.group(2),nameEmailMatch.group(3))
							writer.writerow( (parsed_json['Date'],nameEmailMatch.group(1),nameEmailMatch.group(2),nameEmailMatch.group(3),category,parsed_json['Subject']) )

							#print(parsed_json['Date'])
					except:
						for element in parsed_json['To']:
							justEmailMatch = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", element) 
							#print(justEmailMatch.group(1))
							nameMess = element.replace(justEmailMatch.group(1), "")
							writer.writerow( (parsed_json['Date'],'',nameMess,justEmailMatch.group(1),category,parsed_json['Subject']) )
						l.write(line  + '\n\n')
#						writer.writerow( (parsed_json['Date'],'','',element,parsed_json['Subject']) )


				except:
					l.write(line  + '\n\n')
				
					pass    
			else:
#			elif 'info@artandfeminism.org' or 'info@art.plusfeminism.org' or 'artandfeminismwiki@gmail.com' in parsed_json['From']:
				try:
#					print('else')
					o.write('\n')
#					o.write(parsed_json[outKey]  + '\n')
#					print(parsed_json['X-Originating-IP'])
#					print(parsed_json['From'])
				except:
					l.write(line  + '\n\n')
					pass 

#			else:
#				print('UH OH UH OH UH OH UH OH UH OH UH OH UH OH UH OH UH OH UH OH ')   
		i.close()
		o.close()
		l.close()

