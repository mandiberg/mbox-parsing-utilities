These Python scripts parse mbox mail files. 

One turns the mbox into json. It is modified from Mining the Social Web , 2nd Edition by Matthew A. Russell
https://www.safaribooksonline.com/library/view/mining-the-social/9781449368180/ch06.html

The second reads a JSONified mbox file, and writes selected values to a CSV. 
Right now it is set up to output a list of all email addresses that appear in the "To" field in sent message 
(e.g. Everyone I have ever emailed)
It also adds some category info based of some simple regex keyword searches
