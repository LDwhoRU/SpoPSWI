from flask import Blueprint, render_template, request
from timeit import Timer
# import time
from apscheduler.schedulers.background import BackgroundScheduler

main = Blueprint('main', __name__)

# Variables
fsecond = 1
fminute = 60
fhour = 3600
fday = 86400

dday = 1
dmonth = 30
dyear = 365

days_ago = 365


@main.route('/', methods=['GET', 'POST'])
def index():

	frequency_input = 30 
	frequency_select = 'Minutes' 
	days_ago_input = 6 
	days_ago_select = 'Months' 

	
	spotify_output = ' '
	user_credentials = ' '
	
	if request.method == 'POST':	
		if request.form.get('login', None) == 'Login':
			try:
				from spswi.main.backend import Spotify_Scrape, token
				spotifyscrape = Spotify_Scrape(token)
				spotifyscrape.userAuthentication()
				
			except ImportError:
				from spswi.main.backend import Spotify_Scrape, token
				spotifyscrape = Spotify_Scrape(token)
				blank = spotifyscrape.pullArtists()
			
		if request.form.get('url_submit', None) == 'Authorise':
			try:
				auth_url = request.form.get('url_submit', None, type=str)
				print(auth_url)
			except:
				pass

		if request.form.get('search_artists', None) == 'Search Artist Name':
			from spswi.main.backend import Spotify_Scrape, token
			spotifyscrape = Spotify_Scrape(token)
			spotify_output = spotifyscrape.testSearch()
			print(spotify_output)

		if request.form.get('followed_artists', None) == 'Pull Followed Artists':
			from spswi.main.backend import Spotify_Scrape, token
			spotifyscrape = Spotify_Scrape(token)
			spotify_output = spotifyscrape.pullArtists()
			print(spotify_output)

		if request.form.get('apply_settings', None) == 'Apply Settings':
			
			try:
				frequency_input = request.form.get('frequency_input', 30, type=int)
			except BaseException as error:
				print('error 1: ' + str(error))

			try:
				frequency_select = str(request.form['frequency_select'])
			except BaseException as error:
				print('error 2: ' + str(error))          

			try:
				days_ago_input = request.form.get('days_ago_input', 6, type=int)
			except BaseException as error:
				print('error 3: ' + str(error))

			try:
				days_ago_select = str(request.form['days_ago_select'])
			except BaseException as error:
				print('error 4: ' + str(error))

			global days_ago

			try:
				if days_ago_select == 'Days':
					days_ago = days_ago_input * dday
					print(days_ago)

				elif days_ago_select == 'Months':
					days_ago = days_ago_input * dmonth
					print(days_ago)

				elif days_ago_select == 'Years':
					days_ago = days_ago_input * dyear
					print(days_ago)

			except:
				pass

			try:
				if frequency_select == 'Seconds':
					frequency = frequency_input * fsecond

				elif frequency_select == 'Minutes':
					frequency = frequency_input * fminute

				elif frequency_select == 'Hours':
					frequency = frequency_input * fhour

				elif frequency_select == 'Days':
					frequency = frequency_input * fday

			except:
				pass

			def playlistScraper():
				from spswi.main.backend import Spotify_Scrape, token
				spotifyscrape = Spotify_Scrape(token)
				try:
					spotifyscrape.user.playlistAdd()
				except KeyError:
					spotifyscrape.user.playlistAdd()
				except:
					pass

			scheduler = BackgroundScheduler()
			scheduler.start()

			scheduler.add_job(playlistScraper, 'interval', seconds = float(frequency))

	return render_template('primary.html', frequency_input=frequency_input, frequency_select=frequency_select, days_ago_input=days_ago_input, days_ago_select=days_ago_select, spotify_output=spotify_output)
