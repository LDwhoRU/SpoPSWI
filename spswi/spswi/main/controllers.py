from flask import Blueprint, render_template, request
import sys
import os
#import shed, time


days_ago = 365



main = Blueprint('main', __name__)

# Variables
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

	frequency_input = 30
	frequency_select = 'Minutes'
	days_ago_input = 2
	days_ago_select = 'Months'

	
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
			global


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
				frequency_input = (request.form['frequency_input']).rstrip()
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
				days_ago_input = (request.form['days_ago_input']).rstrip()
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

			

	
	
	return render_template('primary.html', frequency_input=frequency_input, frequency_select=frequency_select, days_ago_input=days_ago_input, days_ago_select=days_ago_select, spotify_output=spotify_output)
