#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()

import files
import match
import img_proc
import sys


try:
	form = cgi.FieldStorage()
	fn = form.getvalue('picture_name')
	cat_id = form.getvalue('selected')
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
	path = '../user_uploads/' + fn
	path = img_proc.pre_processing(path)

	ids, kps, des = files.get_categ_kp_db(cat_id)
	# data to be processed and displayed in the response page
	data_to_be_displayed = match.get_best_matches(path, ids, kps, des)
	data = ""
	nrmatch = ""
	for id in data_to_be_displayed:
		data = data + str(id[0]) + ";"
		nrmatch = nrmatch + str(id[1]) + ";"

	print "Content-type: text/html"
	print
	print "<html><head>"
	print "</head><body>"

	# hidden form containing the data to be redirected to the response page
	print "<form method='post' action='/app_dev.php/responsePage' id='frm'>"

	print "<input type=\"hidden\" name=\"matches\" value=\"" + data + "\"/>"
	print "<input type=\"hidden\" name=\"nrmatches\" value=\"" + nrmatch + "\"/>"
	print "<input type=\"hidden\" name=\"userphoto\" value=\"" + fn + "\"/>"

	print "<noscript><input type='submit' value='Click here if you are not redirected.'/></noscript>"
	print "</form>"

	# auto-submit hidden form
	print "<script language='JavaScript'>"
	print "document.getElementById('frm').submit();"
	print "</script>"

	print "</body></html>"
	print # to end the CGI response headers.