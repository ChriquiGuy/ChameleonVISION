import cv2
from math import *
import numpy as np

class ObjectTracker(object):
    	
	# measurements for mu and motions, U
	measurements = [5., 6., 7., 9., 10.]
	motions = [1., 1., 2., 1., 1.]

	# initial parameters
	measurement_sig = 4.
	motion_sig = 2.
	mu = 0.
	sig = 10000.
    	
		
	# gaussian function
	def f(self, mu, sigma2, x):
    		
		''' 
			f takes in a mean and squared variance, and an input x
			and returns the gaussian value.
		'''

		coefficient = 1.0 / sqrt(2.0 * pi *sigma2)
		exponential = exp(-0.5 * (x-mu) ** 2 / sigma2)
		return coefficient * exponential



	# the update function
	def update(self, mean1, var1, mean2, var2):
    		
		''' 
			This function takes in two means and two squared variance terms,
			and returns updated gaussian parameters.
		'''
		# Calculate the new parameters
		new_mean = (var2*mean1 + var1*mean2)/(var2+var1)
		new_var = 1/(1/var2 + 1/var1)
		
		return [new_mean, new_var]



	# the motion update/predict function
	def predict(self, mean1, var1, mean2, var2):
		
		''' 
			This function takes in two means and two squared variance terms,
			and returns updated gaussian parameters, after motion.
		'''

		# Calculate the new parameters
		new_mean = mean1 + mean2
		new_var = var1 + var2
		
		return [new_mean, new_var]
    	


	def find_tracker_rects(self, current_frame, motion_boxes, result_frame):
		x = 1
