from flask import Blueprint, render_template, request
from timeit import Timer
import time
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
url = "http://localhost:8888/callback/"

days_ago = ' '

master_token = ''

@main.route('/', methods=['GET', 'POST'])
def index():

	

	frequency_input = 2 
	frequency_select = 'Seconds' 
	days_ago_input = 6 
	days_ago_select = 'Months' 

	
	spotify_output = ' '
	user_credentials = ' '
	token_info = ''
	access_token = ''
	

	

	# User token data
	def fetch_sp_oauth():
		from spswi.main.backend import userAuthentication
		user_auth = userAuthentication()
		get_data = user_auth.fetch_user_auth()
		return get_data

	def fetch_token(sp_oauth,url):
		global access_token
		#print('fetching token')
		token_info = sp_oauth.get_cached_token()
		if token_info:
			access_token = token_info#['access_token']
		else:
			code = sp_oauth.parse_response_code(url)
			if code:
				try:
					token_info = sp_oauth.get_access_token(code)
					access_token = token_info#['access_token']
					return access_token
				except:
					#print('exception ' + str(access_token))
					return access_token
		try:
			#print(access_token)
			return access_token
		except:
			return

	def check_url(sp_oauth,found=False):
			#global master_token
			url = request.url
			if 'code' in str(url):
				master_token = fetch_token(sp_oauth,url)
				found = True
				return master_token
			url_scheduler = BackgroundScheduler()
			url_scheduler.start()
			try:
				if found == False:
					url_scheduler.add_job(url, 'interval', seconds = 3)
			except LookupError:
				pass
			

	def getSPOauthURI(sp_oauth):
		auth_url = sp_oauth.get_authorize_url()
		check_url(sp_oauth)
		return auth_url
		
	
	sp_oauth = fetch_sp_oauth()
	auth_url = getSPOauthURI(sp_oauth)
	#user_token = fetch_token(sp_oauth)



	if request.method == 'POST':	

		if request.form.get('search_artists', None) == 'Search Artist Name':
			from spswi.main.backend import Spotify_Scrape
			master_token = fetch_token(sp_oauth,url)
			# print('fetching ' + str(master_token))
			spotifyscrape = Spotify_Scrape(master_token)
			spotify_output = spotifyscrape.testSearch()
			print(spotify_output)

		if request.form.get('followed_artists', None) == 'Pull Followed Artists':
			from spswi.main.backend import Spotify_Scrape
			master_token = fetch_token(sp_oauth,url)
			print('fetching ' + str(master_token))
			spotifyscrape = Spotify_Scrape(master_token)
			spotify_output = spotifyscrape.pullArtists()
			print(spotify_output)

		if request.form.get('apply_settings', None) == 'Apply Settings':
			
			try:
				frequency_input = request.form.get('frequency_input', frequency_input, type=int)
			except BaseException as error:
				print('error 1: ' + str(error))

			try:
				frequency_select = str(request.form['frequency_select'])
			except BaseException as error:
				print('error 2: ' + str(error))          

			try:
				days_ago_input = request.form.get('days_ago_input', days_ago_input, type=int)
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
					return days_ago
					print(days_ago)

				elif days_ago_select == 'Months':
					days_ago = days_ago_input * dmonth
					return days_ago
					print(days_ago)

				elif days_ago_select == 'Years':
					days_ago = days_ago_input * dyear
					return days_ago
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
			
			def newPlaylist(playlist_id,spotifyscrape):
				with open('playlist.txt', 'w') as check:
							check.write(playlist_id)
				print("new playlist")
				artist_uri = spotifyscrape.uriArtist()
				album_uri = spotifyscrape.uriAlbums(artist_uri, days_ago)
				track_uri = spotifyscrape.uriTracks(album_uri)
				add_playlist = spotifyscrape.addPlaylist(track_uri,playlist_id)
				#print(artist_uri)
				#print(album_uri)
				#print(track_uri)
				print(add_playlist)


			def playlistScraper():
				from spswi.main.backend import Spotify_Scrape
				master_token = fetch_token(sp_oauth,url)
				spotifyscrape = Spotify_Scrape(master_token)
				playlist_id = spotifyscrape.checkPlaylists()
				print("Current playlist is: " + playlist_id)
				try:
					with open('playlist.txt', 'r') as check:
						cached_id = check.read()
					#print("Old id is : " + cached_id)
				except FileNotFoundError:
					print("not found")
				try:
					if playlist_id == cached_id:
						print("Same playlist")
					else:
						newPlaylist(playlist_id,spotifyscrape)
				except:
					newPlaylist(playlist_id,spotifyscrape)

			playlistScraper()

			scheduler = BackgroundScheduler()
			scheduler.start()

			scheduler.add_job(playlistScraper, 'interval', seconds = float(frequency))

	return render_template('primary.html', frequency_input=frequency_input, frequency_select=frequency_select, days_ago_input=days_ago_input, days_ago_select=days_ago_select, spotify_output=spotify_output, auth_url=auth_url)
