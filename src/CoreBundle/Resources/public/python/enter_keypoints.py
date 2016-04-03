#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()
import os
import match
from files import insert_photo, create_dir
from aux import name_gen
import sys

try:
	form = cgi.FieldStorage()
	fileitem = form['file']
	id_prod = form['product']
	id_categ = form['category']
except:
	print "Content-type: text/html"
	print
	print "<html><head>"
	print "</head><body>"
	print "<h1>There was an error</h1>"
	exctype, value = sys.exc_info()[:2]
	print "<p>Error type: {0}, value: {1}</p>".format(exctype, value)
	print "</body></html>"
	print 
else:
	if fileitem.filename != "":
		create_dir()
		fn = name_gen()
		ext = os.path.splitext(fileitem.filename)[1]
		img = '../files/'+ fn + ext;
		f = open(img, 'wb')
		f.write(fileitem.file.read());
		f.close()
		rez = insert_photo(img, id_prod.value, id_categ.value)

		if rez == 1:
			message = "Keypoints added successfully."
		else:
			message = "This photo is already saved" + str(rez)
		
		print "Content-type: text/html"
		print
		print "<html><head>"
		print "</head><body>"

		print "<form method='post' action='/app_dev.php/updateDatabase' id='frm'>"

		print "<input type='hidden' name='addKeypoint_message' value='" + message + "'/>"

		print "<noscript><input type='submit' value='Click here if you are not redirected.'/></noscript>"
		print "</form>"

		# auto-submit hidden form
		print "<script language='JavaScript'>"
		print "document.getElementById('frm').submit();"
		print "</script>"
		
		print # to end the CGI response headers.