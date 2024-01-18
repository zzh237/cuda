#!/usr/bin/python3

# ENTRYPOINT for Dockerfile

# Dependencies
import logging
import os
from util import print_stderr, send_feedback, print_stdout
import re


def main(part_id, filename):
	# Find the learner's submission  ----------------------------------------------
	project_location = "/shared/submission/"
	
	# Each partId is evaluated one at a time; thus, only one submission file will be stored
	# at a time in the /shared/submission/ directory.
	file_location = project_location + filename
	
	feedback = f"Processing part: {part_id} with file: {file_location}.\n"

	score, feedback = use_regex_on_file(part_id=part_id, file_location=file_location, feedback=feedback)
	
	feedback = f"{feedback}Your grade will be {score * 100}.\n"
	send_feedback(score, feedback)


def use_regex_on_file(part_id, file_location, feedback):
	# Open file for reading
	fo = open(file_location)
	
	try:
		line = fo.readline()
		input_data = line.split(' ')
		input_data = input_data[1:]
		print("input_data: ", input_data)
		
		line = fo.readline().strip()
		search_value = line.split(' ')
		search_value = search_value[3]
		print("search_value: ", search_value)
		
		line = fo.readline()
		found_index = line.split(' ')
		found_index = int(found_index[2])
		print("found_index: ", found_index)

		score = 0.0
		if part_id == 'IzONJ' and found_index == -1:
			score = 0.0
		else:
			try:
				actual_found_index = input_data.index(search_value)
				print("actual_found_index: ", actual_found_index)
				if actual_found_index == found_index:
					feedback = f"{feedback}\nThe search kernel found the search value at the actual location.\n"
					score = 1.0
				else:
					feedback = f"{feedback}\nThe search kernel did not find the search value at the actual location.\n"
			except ValueError:
				if found_index == -1:
					score = 1.0
					feedback = f"{feedback}\nThe search kernel was correct that the search value was not in the input data.\n"
				else:
					feedback = f"{feedback}\nThe search value is not in the input data but the submitted search kernel found something."
					feedback = f"{feedback}\nThis part will have a score of 0."
	except os.error:
		feedback = f"{feedback}\nAn exception occured while parsing the output of search.exe.\n"
		feedback = f"{feedback}\nThe 1st line should start with 'Data:' and then have input data.\n"
		feedback = f"{feedback}\nThe 2nd line should start with 'Searching for value:' and then has the search value.\n"
		feedback = f"{feedback}\nThe 3rd line should start with 'Found Index:' and then has actual found index.\n"
	
	print("score: ", score)

	fo.close()
	return score, feedback


if __name__ == '__main__':
	try:
		part_id = os.environ['partId']
		filename = os.environ['filename']
	except Exception as e:
		print_stderr("Please provide the part_id.\n")
		send_feedback(0.0, "Please provide the part_id.\n")
	else:
		main(part_id=part_id, filename=filename)
