import string
import random

###
# name_gen() generates a random string consisting of alpha-numerics
# with the length of size (set to 6 by default)
###
def name_gen(size=6):
	chars = string.ascii_uppercase + string.digits
	return ''.join(random.choice(chars) for _ in range(size))