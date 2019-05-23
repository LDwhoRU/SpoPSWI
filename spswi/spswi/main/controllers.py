from flask import Blueprint, render_template, request
import sys
import os
import numpy as np
#import shed, time




main = Blueprint('main', __name__)

# Variables
day = 1
month = 30
year = 365




def replace_line(line_num, text):
	lines = open('config', 'r').readlines()
	lines[line_num] = text
	out = open('config', 'w')
	out.writelines(lines)
	out.close()

def read_file(line_num):
	lines = open('config', 'r').readlines()
	return lines[line_num]


config_array = []
	


@main.route('/', methods=['GET', 'POST'])
def index():

	global config_array
	with open('config') as inputfile:
		for line in inputfile:
			config_array.append(line.split(','))

	print(config_array)
	
	fi = config_array[0][0]
	fs = config_array[0][1]
	di = config_array[0][2]
	ds = config_array[0][3]


	frequency_input = fi
	frequency_select = fs
	days_ago_input = di
	days_ago_select = ds

	
	spotify_output = ' '
	user_credentials = ' '

	if request.method == 'GET':
		pass
		# if request.form.get('login', None) == 'Login':
		# 	from spswi.main.backend import Spotify_Scrape, token
		# 	spotifyscrape = Spotify_Scrape(token)
		# 	spotifyscrape.pullArtists()

		
			


	if request.method == 'POST':	
		if request.form.get('login', None) == 'Login':
			from spswi.main.backend import Spotify_Scrape, token
			spotifyscrape = Spotify_Scrape(token)
			# global spotify_output
			blank = spotifyscrape.pullArtists()
			
		if request.form.get('url_submit', None) == 'Authorise':
			pass


		if request.form.get('search_artists', None) == 'Search Artist Name':
			from spswi.main.backend import Spotify_Scrape, token
			spotifyscrape = Spotify_Scrape(token)
			# global spotify_output
			spotify_output = spotifyscrape.testSearch()
			print(spotify_output)

		if request.form.get('followed_artists', None) == 'Pull Followed Artists':
			from spswi.main.backend import Spotify_Scrape, token
			spotifyscrape = Spotify_Scrape(token)
			# global spotify_output
			spotify_output = spotifyscrape.pullArtists()
			print(spotify_output)

		if request.form.get('apply_settings', None) == 'Apply Settings':
			try:
				frequency_input = request.form.get('frequency_input', '30', type=int)
				# replace_line(0, frequency_input)
				print(frequency_input)
			except BaseException as error:
				print('error 1: ' + str(error))

			try:
				frequency_select = str(request.form['frequency_select'])
				# replace_line(1, frequency_select)
				print(frequency_select)
			except BaseException as error:
				print('error 2: ' + str(error))          

			try:
				days_ago_input = request.form.get('days_ago_input', '6', type=int)
				# replace_line(2, days_ago_input)
				print(days_ago_input)
			except BaseException as error:
				print('error 3: ' + str(error))

			try:
				days_ago_select = str(request.form['days_ago_select'])
				# replace_line(3, days_ago_select)
				print(days_ago_select)
			except BaseException as error:
				print('error 4: ' + str(error))

			
			config_array = [frequency_input, frequency_select, days_ago_input, days_ago_select]
			with open('config', 'w') as f:
				for item in config_array:
					f.write("%s," % item)

			global days_ago
			try:
				if days_ago_select == 'Days':
					days_ago = days_ago_input * days
					print(days_ago)
				elif days_ago_select == 'Months':
					days_ago = days_ago_input * month
					print(days_ago)
				elif days_ago_select == 'Years':
					days_ago = days_ago_input * year
					print(days_ago)
			except:
				pass
	
	return render_template('primary.html', frequency_input=frequency_input, frequency_select=frequency_select, days_ago_input=days_ago_input, days_ago_select=days_ago_select, spotify_output=spotify_output)
