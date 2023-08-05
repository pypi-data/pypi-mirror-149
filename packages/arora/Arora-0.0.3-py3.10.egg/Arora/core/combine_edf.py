import pyedflib as edf


def combine(file1, file2):
	# Take in both edf files
	# Open them both in PyEDFlib
	# Iterate through both files and find discrepancies
	# Create new file and add both to that one
	# If there already exists one signal with same name,
	# 	- create a new name for the signal to be able to compare the two
	# Check for min and max of the file
	# Return the new file

	if edf.highlevel.compare_edf(file1, file2):
		raise Exception("The contents of this file are the same")


	return None
