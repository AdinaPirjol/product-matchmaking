import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import cPickle as pickle
from joblib import Parallel, delayed
import md5
import bz2
from PIL import Image
import os


###
# get_matches() matches the keypoints and descriptors from one image
# to another and returns the number of good matches after filtering
# Input:
# kp1(Keypoints object),des1(numpy array) = keypoints and descriptors for first image
# kp2(Keypoints object),des2(numpy array) = keypoints and descriptors for second image
# Output:
# count_good_matches(int) = number of good matches
###
def get_matches(kp1, des1, kp2, des2):
	# initiating the SIFT() object for matching
	orb = cv2.SIFT();

	# creating necessary arguments for FLANN algorithm
	FLANN_INDEX_KDTREE = 0;
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5);
	search_params = dict(checks=50);

	# matching kps and descriptors using the FLANN algorithm with K-Nearest-Neighbors method
	flann = cv2.FlannBasedMatcher(index_params, search_params);
	matches = flann.knnMatch(des1, des2, k=2);

	# filtering matches by distance
	# the 0.65 value turned out to be the best value for filtering
	count_good_matches = 0
	for i, (m,n) in enumerate(matches):
	    if m.distance < 0.65*n.distance:
	        count_good_matches += 1
	return count_good_matches



###
# get_kp_desc extracts keypoints and descriptors from an image
# Input:
# img = path to image
# Output:
# kp(Keypoints object), des(numpy array) = keypoints and descriptors extracted
# -1,-1 if image is corrupted
###
def get_kp_desc(img):
	img = cv2.imread(img, 0);
	orb = cv2.SIFT();
	try:
		kp, des = orb.detectAndCompute(img, None);
	except cv2.error as err:
		print "The picture could not be processed. It is probably deteriorated.<br/> Error:<br/>"
		print err
		print "<br/>"
		return -1, -1
	else:
		return kp, des;

###
# pickle_kp serializes keypoints and descriptors and then
# compresses them before saving them to a file path generated
# using id_prod and id_categ
# Input:
# kp(Keypoints object), desc(numpy array) = keypoints and descriptors to pickle
# id_prod(int) = product id
# id_categ(int) = category id
# Output:
# hashish(string) = unique hash for each pickle
###
def pickle_kp(kp, desc, id_prod, id_categ):
	i = 0;
	temp_array = [];
	for point in kp:
		temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, desc[i]);
		i += 1;
		temp_array.append(temp);
	string = pickle.dumps(temp_array);
	m = md5.new()
	m.update(string)
	hashish = m.hexdigest()

	fn = id_prod + '_' + hashish + '.bz2'
	dir = '../keypoints/' + id_categ
	file_path = dir + '/' + fn

	if not os.path.isdir(dir):
		os.mkdir(dir)
		kp_content = pickle.dumps(temp_array)
		compress(kp_content, file_path)
		return hashish
	else:
		if not os.path.exists(file_path):
			kp_content = pickle.dumps(temp_array)
			compress(kp_content, file_path)
			return hashish
		else:
			return -1

###
# Decompresses and extracts keypoints that were previously saved in
# a file
# Input:
# path(string) = path to file that needs to be decompressed/unpickled
# Output:
# kp(Keypoints object), des(numpy array) = raw keypoints and descriptors
###
def unpickle_kp(path):
	kp = []
	desc = []

	kp_content = decompress(path)
	array = pickle.loads(kp_content)

	for point in array:
		temp_feature = cv2.KeyPoint(x = point[0][0], 
									y = point[0][1],
									_size = point[1],
									_angle = point[2],
									_response = point[3],
									_octave = point[4],
									_class_id = point[5]);
		temp_desc = point[6];
		kp.append(temp_feature);
		desc.append(temp_desc);
	return kp, np.array(desc);

###
# decompress kp and descr using bz2 module
# Input: path(string) = path of the saved kps and descr
###
def decompress(path):
	f = open(path, "rb")
	kp_content = f.read()
	kp_content = bz2.decompress(kp_content)
	f.close()
	return kp_content

###
# compress kp and descr using bz2 module
# Input:
# kp_content(string) = pickled keypoints and descriptors to be compressed
# file_path(string) = path where the keypoints and descriptors will be saved
###
def compress(kp_content, file_path):
	kp_content = bz2.compress(kp_content, 1)
	bz2_file = open(file_path, "wb")
	bz2_file.write(kp_content)
	bz2_file.close()


###
# Generator function used to parallelize the keypoint matching
# process in get_best_matches() 
# Input:
# array(list) = list of the keypoints and descriptors of two
#         images and the corresponding product ids
# Output:
# tuple of the form (product id,number of matches)
# on on a specific product
# ids(int), no_matches(int)
###
def match_gen(array):
	src_kp = list_to_kp(array[0])
	src_des = array[1]
	kps = list_to_kp(array[2])
	des = array[3]
	ids = array[4]

	no_matches = get_matches(src_kp, src_des, kps, des)
	if no_matches > 0:
		return (ids, no_matches)
	return (0, 0)

###
# Converts a keypoint object to a list that can be pickled for the
# parallelizing process
# Input:
# kp = cv2.Keypoint object
# Output:
# temp_arr = list of tuples containing 6 features for each keypoint
###
def kp_to_list(kp):
	temp_arr = []
	for point in kp:
		temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id)
		temp_arr.append(temp)

	return temp_arr

###
# Converts a keypoint list to a keypoint object
# Input:
# kps = list of keypoints
# Output:
# kp = cv2.Keypoint object
###
def list_to_kp(kps):
	kp = []
	for point in kps:
		temp_feature = cv2.KeyPoint(x = point[0][0], 
									y = point[0][1],
									_size = point[1],
									_angle = point[2],
									_response = point[3],
									_octave = point[4],
									_class_id = point[5]);
		kp.append(temp_feature)
	return kp

###
# Obtains the number of matches for each photo we have stored
# and returns the one that has the most matches as the result
# Input:
# img(string) = path to user image
# ids, kps, des = lists of all ids, keypoints and descriptors to match with
# ids(int[]), kps(cv2.Keypoint obj[]), des(numpy array[]) 
# Output:
# list of tuples of the form (id, no_matches) 
# with the first number_of_result best matches
# Configuration:
# number_of_result = number of results to return
# n_jobs = number of processes to use for parallel execution
###
def get_best_matches(img, ids, kps, des):
	number_of_results = 3

	src_kp, src_des = get_kp_desc(img)
	os.remove(img)
	matches = []

	matches = Parallel(n_jobs=-1)(delayed(match_gen)([kp_to_list(src_kp), src_des, kp_to_list(kps[i]), des[i], ids[i]]) for i in range(len(ids)))
	
	# remove product ids that have 0 matches
	for elem in matches[:]:
		if elem[1] == 0:
			matches.remove(elem)

	# sort by ids in order to remove duplicate ids for pics with less matches of the same product
	matches = sorted(matches, key=lambda tup: tup[0])

	# and remove possible product id duplicates
	# that may appear from the match-making algorithm applied 
	# on different picture keypoints of the same product
	s = set()
	for elem in matches[:]:
		if elem[0] in s:
			matches.remove(elem)
		else:
			s.add(elem[0])

	# sort by number of matches
	matches = sorted(matches, key=lambda tup: tup[1])
	matches.reverse()

	# return the first number_of_results most matching
	return [i for i in matches[:number_of_results]]
