#!/usr/bin/env python

print "Content-type: text/html"
print
print "<html><head>"
print ""
print "</head><body>"
 
import cv2
import match
import os
from datetime import datetime

###
# Different compression methods for any further use
###

# method 1 - gzip
def gzip_compr(file_hash):
	print '<b>Method 1: using gzip</b><br>'
	f = open('../keypoints/' + file_hash + '.p', 'rb')
	time = datetime.now()
	import gzip
	gzip_file = gzip.open('../keypoints/' + file_hash + '.p.gz', mode='wb', compresslevel=9)
	gzip_file.writelines(f)
	gzip_file.close()
	f.close()

	t1 = datetime.now() - time
	print 'Time spent compressing gzip: %s<br>' % (datetime.now() - time)
	gzib_size = os.stat('../keypoints/' + file_hash + '.p.gz').st_size
	print 'gzip compressed .p.gz file size: %s kb<br>' % (gzib_size/1024)
	print 'Shrinked %s times<br>' % str(round(orig_size*1.0/gzib_size, 2))

	time = datetime.now()
	f = gzip.open('../keypoints/' + file_hash + '.p.gz', 'rb')
	file_content = f.read()
	f.close()

	t = datetime.now() - time
	print 'Time spent decompressing gzip: %s<br>' % (datetime.now() - time)
	return (gzib_size/1024,round(orig_size*1.0/gzib_size, 2),t,t1)



# method 2 - zlib
def zlib_compr(file_hash):
	print '<b>Method 2: using zlib<br></b>'
	import zlib
	file_content = open('../keypoints/' + file_hash + '.p', 'rb').read()
	time = datetime.now()
	file_content = zlib.compress(file_content, 1)
	zlib_file = open('../keypoints/' + file_hash + '.txt', 'wb')
	zlib_file.write(file_content)
	zlib_file.close()

	t1 = datetime.now() - time
	print 'Time spent compressing zlib: %s<br>' % (datetime.now() - time)
	zlib_size = os.stat('../keypoints/' + file_hash + '.txt').st_size
	print 'zlib compressed .txt file size: %s kb<br>' % (zlib_size/1024)
	print 'Shrinked %s times<br>' % str(round(orig_size*1.0/zlib_size, 2))

	time = datetime.now()
	f = open('../keypoints/' + file_hash + '.txt', 'rb')
	content = f.read()
	file_content = zlib.decompress(content)
	f.close()

	t = datetime.now() - time
	print 'Time spent decompressing zlib: %s<br>' % (datetime.now() - time)
	return (zlib_size/1024,round(orig_size*1.0/zlib_size, 2),t,t1)


# method 3 - bz2
def bz2_compr(file_hash):
	print '<b>Method 3: using bz2<br></b>'
	file_content = open('../keypoints/' + file_hash + '.p', 'rb').read()
	time = datetime.now()
	import bz2
	file_content = bz2.compress(file_content, 1)
	bz2_file = open('../keypoints/' + file_hash + '.bz2.txt', 'wb')
	bz2_file.write(file_content)
	bz2_file.close()

	t1 = datetime.now() - time
	print 'Time spent compressing bz2: %s<br>' % (datetime.now() - time)
	bz2_size = os.stat('../keypoints/' + file_hash + '.bz2.txt').st_size
	print 'bz2 compressed .txt file size: %s kb<br>' % (bz2_size/1024)
	print 'Shrinked %s times<br>' % str(round(orig_size*1.0/bz2_size, 2))

	time = datetime.now()
	f = open('../keypoints/' + file_hash + '.bz2.txt', 'rb')
	content = f.read()
	file_content = bz2.decompress(content)
	f.close()

	t = datetime.now() - time
	print 'Time spent decompressing bz2: %s<br>' % (datetime.now() - time)
	return (bz2_size/1024,round(orig_size*1.0/bz2_size, 2),t,t1)