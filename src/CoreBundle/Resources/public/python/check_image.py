#!/bin/usr/python

import imghdr
import sys
import os

class ImageChecking:
	def checkType(self, img):
		accepted = ['png', 'jpg', 'jpeg']
		type = imghdr.what(img)
		if type in accepted:
			return True
		return False

	def getSize(self, img):
		size = os.path.getsize(img)
		return size/(1024*1024)

	def checkFile(self, img):
		file = img
		typeOk = self.checkType(file)
		size = self.getSize(file)

		if typeOK == True and size <= 5:
			return True
		else
			return False