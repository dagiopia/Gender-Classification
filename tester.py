#!/usr/bin/env python 
from sklearn.svm import LinearSVC
import pickle
import numpy as np 
import sys
import os
from utilities import * 

MALE_CLASS = 0
FEMALE_CLASS = 1
current_class = 0

def classify(file_name, male_label, svm_model):
	sample_rate, data = wavfile.read(file_name)
	data_no_silence = no_silence(data, sample_rate)
	features = feature_extraction(data_no_silence, sample_rate, sample_rate*0.05, sample_rate*0.025)
	window_pred = svm_model.predict(np.transpose(features)).tolist()
	maleness = window_pred.count(male_label)
	maleness = (float(maleness) / len(window_pred))
	return MALE_CLASS if maleness > 0.5 else FEMALE_CLASS
	


if len(sys.argv) != 3:
	print "Error command"
	print "		python "+ sys.argv[0]  +" [test-male-directory] [test-female-directory]"
	exit()


svm = pickle.load(open("test/model_pickle.pkl", 'r'))
for sex_class in range(1, len(sys.argv)):
	
	error_class = 0
	num_test = 0
	correct_class = 0
	class_name = sys.argv[sex_class].split('/')[-2]
	
		
	print "Testing for class =====  " + class_name + "  [" + str(current_class) + "]"
	file_counter = 0
	file_list = os.listdir(sys.argv[sex_class])
	
	for file_name in file_list:
		predicted_class = classify(sys.argv[sex_class] + file_name, 0, svm)
		if predicted_class == current_class:
			correct_class += 1
		else:
			error_class += 1
		num_test += 1
		
	print "**** END OF TEST FOR CURRENT CLASS *****"
	print "Number of Correct Classifications = " + str(correct_class)
	print "Number of Error Classifications   = " + str(error_class)
	print "Number of tests in total          = " + str(num_test)
	print "Total Accuracy                    = " + str((float(correct_class)/num_test)*100)
	print "\n\n"
	current_class += 1

