from flask import Blueprint, render_template, request
#from spswi.main.functions import *
import sys
import os
#from spswi.backend import pullArtists

main = Blueprint('main', __name__)

# Time period variables
day = 1
month = 30
year = 365

def replace_line(file_name, line_num, text):
	lines = open(file_name, 'r').readlines()
	lines[line_num] = text
	out = open(file_name, 'w')
	out.writelines(lines)
	out.close()

def read_file(file_name, line_num):
	lines = open(file_name, 'r').readlines()
	return lines[line_num]
	out.close()



@main.route('/', methods=['GET', 'POST'])
def index():

	frequency_input = int(read_file('config', 0))
	frequency_select = read_file('config', 1)
	days_ago_input = int(read_file('config', 2))
	days_ago_select = read_file('config', 3)

	#replace_line(os.path.join(sys.path[0] + '/spswi/main/config.txt'), 0, frequency_input)
	if request.method == 'POST':

		if request.form['apply_settings'] == 'Apply Settings':
			try:
				frequency_input = (request.form[frequency_input]).rstrip()
				replace_line('config', 0, frequency_input)
				print(frequency_input)
			except BaseException as error:
				print('error 1: ' + str(error))

			try:
				frequency_select = str(request.form['frequency_select'])
				replace_line('config', 1, (frequency_select + '\n'))
				print(frequency_select)
			except BaseException as error:
				print('error 2: ' + str(error))

			try:
				days_ago_input = (request.form['days_ago_input']).strip('\n')
				replace_line('config', 2, days_ago_input)
				print(days_ago_input)
			except BaseException as error:
				print('error 3: ' + str(error))

			try:
				days_ago_select = str(request.form['days_ago_select'])
				replace_line('config', 3, days_ago_select)
				print(days_ago_select)
			except BaseException as error:
				print('error 4: ' + str(error))


	return render_template('primary.html', frequency_input=frequency_input, frequency_select=frequency_select, days_ago_input=days_ago_input, days_ago_select=days_ago_select)
