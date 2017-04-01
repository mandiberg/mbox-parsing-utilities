import sys
import mailbox
import email
import quopri
import json
import time

# This script comes from
# Mining the Social Web , 2nd Edition by Matthew A. Russell
# https://www.safaribooksonline.com/library/view/mining-the-social/9781449368180/ch06.html
# I have modified it only to get it to work on my machine (fixed try/except at bottom)
# I also added in a line to rm message subject, as I only wanted metadata

# need to import bSoup, and then strip HTML which will hopefully fix parse errors
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
#from dateutil.parser import parse
import codecs

#MBOX = 'gc/Inbox.mbox/mbox'
#OUT_FILE = 'gc/gc.mbox.json'

MBOXname = 'mcom'
#MBOX = MBOXname + '/All Mail.mbox/trim.mbox'
MBOX = 'mcom.mbox'
#OUT_FILE = MBOXname + '/' + MBOXname + '.mbox.json'
OUT_FILE =  MBOXname + '.mbox.json'


def remove_non_ascii_1(text):

    return ''.join(i for i in text if ord(i)<128)


def cleanContent(msg):

    # Decode message from "quoted printable" format
    msg = remove_non_ascii_1(msg)

    msg = quopri.decodestring(msg)
        
    # Strip out HTML tags, if any are present.
    # Bail on unknown encodings if errors happen in BeautifulSoup.
    try:
        soup = BeautifulSoup(msg, 'html.parser')
    except:
        return ''
    return ''.join(soup.findAll(text=True))

# There's a lot of data to process, and the Pythonic way to do it is with a 
# generator. See http://wiki.python.org/moin/Generators.
# Using a generator requires a trivial encoder to be passed to json for object 
# serialization.

class Encoder(json.JSONEncoder):
    def default(self, o): return  list(o)

# The generator itself...
def gen_json_msgs(mb):
    while 1:
        msg = mb.next()
        if msg is None:
            break
        try:
	        yield jsonifyMessage(msg)
    	except:
	    	pass
 
def jsonifyMessage(msg):
    json_msg = {'parts': []}
    for (k, v) in msg.items():
        json_msg[k] = v.decode('utf-8', 'ignore')
#        json_msg[k] = v.decode('string_escape')

    # The To, Cc, and Bcc fields, if present, could have multiple items.
    # Note that not all of these fields are necessarily defined.

    for k in ['To', 'Cc', 'Bcc']:
        if not json_msg.get(k):
            continue
        json_msg[k] = json_msg[k].replace('\n', '').replace('\t', '').replace('\r', '')\
                                 .replace(' ', '').decode('utf-8', 'ignore').split(',')

    for part in msg.walk():
        json_part = {}
        if part.get_content_maintype() == 'multipart':
            continue
            
        json_part['contentType'] = part.get_content_type()
#	print part.get_payload()
        content = part.get_payload(decode=False).decode('utf-8', 'ignore')
        json_part['content'] = cleanContent(content)
#        json_part['content'] = 'this was the content'
         
        json_msg['parts'].append(json_part)
        
    # Finally, convert date from asctime to milliseconds since epoch using the
    # $date descriptor so it imports "natively" as an ISODate object in MongoDB
#    then = parse(json_msg['Date'])
#    millis = int(time.mktime(then.timetuple())*1000 + then.microsecond/1000)
#    json_msg['Date'] = {'$date' : millis}

    return json_msg

mbox = mailbox.UnixMailbox(open(MBOX, 'rb'), email.message_from_file)

# Write each message out as a JSON object on a separate line
# for easy import into MongoDB via mongoimport



f = open(OUT_FILE, 'w')
for msg in gen_json_msgs(mbox):
    try:
		if msg != None:
			f.write(json.dumps(msg, cls=Encoder) + '\n')
    except:
        pass
f.close()