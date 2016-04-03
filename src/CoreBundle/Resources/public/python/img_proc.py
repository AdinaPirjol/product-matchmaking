import cv2
import numpy as np
from sys import argv
from pylab import arange,array,uint8
from PIL import Image
from aux import name_gen
import os
 
###
# Resizes an image to a maximum size of max_size x max_size
# if the image is bigger than max_size x max_size
# Input:
# img(string) = path to image on local disk
# max_size(int) = the maximum width and height the image should have
# Output:
# returns the path to the resized image (if it got resized) or
# the same path that was passed if no modifications were made
###
def image_resize(img, max_size):
	p = Image.open(img)
	w, h = p.size

	if w > max_size or h > max_size:
		ratio = min(max_size/float(w), max_size/float(h))
		new_size = (int(w*ratio), int(h*ratio))
		old_name = img
		p.thumbnail(new_size, Image.ANTIALIAS)
		new_name = "../files/" + name_gen() + ".jpg"
		p.save(new_name, "JPEG")
		os.remove(old_name)
		return new_name
	return img


###
# pre_processing() is the main method to call the 
# denoise, brightness and contrast correction methods
# on the picture uploaded by the user
# Input: path(string) = temporary path to the picture uploaded by the user
# Output: f(string) = path to the processed picture that will be further 
# 					  used in the matchmaking algorithm
###
def pre_processing(path):
	img = cv2.imread(path, 0)
	res = denoise(img)
	res = bright_corr(res)

	f = '../user_uploads/' + name_gen() + '.jpg'
	cv2.imwrite(f, res)
	return f

###
# denoise() - denoising of the input image
# Input: img(numpy.ndarray) = cv2 loaded image
# Output: res(numpy.ndarray) = cv2 denoised image
###
def denoise(img):
	noise_param = 2				#Bigger filter_param value perfectly removes noise but also removes image details, smaller h value preserves details but also preserves some noise
	tmpWindowSize = 7			#templateWindowSize : should be odd. (recommended 7)
	srcWindowSize  = 21			#searchWindowSize : should be odd. (recommended 21)

	#opencv denoise method call
	res = cv2.fastNlMeansDenoising(img,None,noise_param,tmpWindowSize,srcWindowSize)

	return res


###
# bright_corr() method decides whether the image should be lightened or darkened
# based on the average intensity value of the pixels
# Input: img(numpy.ndarray) = cv2 denoised image
# Output: img(numpy.ndarray) = cv2 brightness/contrast corrected image
###
def bright_corr(img):
	# cv2.mean() returns the average value of the pixels in a image
	# range 0-255 (BLACK WHITE) for grayscale images
	# mean - 4 elem vector (for 3 channeled pics)
	mean = cv2.mean(img) 
	maxIntensity = 255.0

	# print "mean is %s" % (str(mean))

	if mean > maxIntensity/2:
		# print "brightness light corr"
		img = bright_corr_light(img)
	else:
		# print "brightness dark corr"
		img = bright_corr_dark(img)

	return img


###
# bright_corr_light() - lightens the image
# Increase intensity such that
# dark pixels become much brighter, 
# bright pixels become slightly bright
# default value used: 0.5
# Input: img(numpy.ndarray) - cv2 denoised image
# Outut: img(numpy.ndarray) - cv2 lightened image
###
def bright_corr_light(img):
	###NEW IMAGE BRIGHTNESS###

	# Image data
	maxIntensity = 255.0 	#depends on dtype of image data
							#for grayscale pics, maxIntensity is 255 (white)

	# Parameters for manipulating image data
	# phi must be bigger or equal to theta (else, some image corruption might appear)
	phi = 1.4
	theta = 1.4

	res = (maxIntensity/phi)*(img/(maxIntensity/theta))**0.6
	res = array(res,dtype=uint8)

	return res


###
# bright_corr_dark() - darkens the image
# Decrease intensity such that
# dark pixels become much darker, 
# bright pixels become slightly dark 
# Input: img(numpy.ndarray) - cv2 denoised image
# Outut: img(numpy.ndarray) - cv2 darkened image
###
def bright_corr_dark(img):
	# Image data
	maxIntensity = 255.0 	#depends on dtype of image data
							#for grayscale pics, maxIntensity is 255 (white)

	# Parameters for manipulating image data
	# phi must be bigger than theta (else, some image corruption might appear)
	phi = 1.4
	theta = 1.4

	res = (maxIntensity/phi)*(img/(maxIntensity/theta))**2
	res = array(res,dtype=uint8)

	return res