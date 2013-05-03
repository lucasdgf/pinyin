"""
	Assignment 3 		Word Segmentation via
				  		the TANGO Algorithm 
				  		
	Coded with love by	Lucas Freitas '15
						Harvard University
"""

import sys
import re
import utils

def segment(filename):
	try:
		input = open(self.input_file, 'r').readlines()
	except IOError:
		print "IOError: could not open", self.input_file
		sys.exit()


def main ():
	# parse command-line arguments
	args = parseArgs(sys.argv)

	# assign values based on arguments
	input = args["-f"]
	output = args["-p"]
	max_n = int(args["-n"])
	threshold = float(args["-t"])

	# create text structure, and then segment text
	text = Text(input, output, max_n, threshold)

	# print precision, recall and number of prediction lines used
	#print "precision %.5f\nrecall %.5f" % (text.precision, text.recall)
	print "\n%d prediction lines used for evaluation" %len(text.original_text)
	
	# plot graph
	#text.plot_graph()

if __name__ == "__main__":
	main()