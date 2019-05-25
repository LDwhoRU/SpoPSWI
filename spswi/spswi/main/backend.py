#from spswi.main.controllers import days_ago

# import modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from spotipy import oauth2
import codecs
import datetime
import random
username = ""

# filter dates
today = datetime.date.today()
time_ago = today - datetime.timedelta(days=365)
print('Filtering from ' + str(time_ago))

class userAuthentication:

    def fetch_user_auth(self):
        # app credentials
        self.cid ="244ce08ff106437f8e7565c2e796f4e3" 
        self.secret = "6e652d745f094973a50ef8204b953828"
        self.username = ""
        self.redirect_url = "http://0.0.0.0:5000/"
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret) 
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        self.scope = """
        user-top-read user-library-modify user-library-read playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-read-email user-read-birthdate user-read-private
        user-follow-read user-follow-modify
        """
        self.fetched_auth = self.oath_authenticator(self.cid,self.secret,self.redirect_url,self.scope)
        #token = util.prompt_for_user_token(username, scope, cid, secret, redirect_url)
        #print(token)
        #if token:
            #sp = spotipy.Spotify(auth=token) # try authentication
            #return token
        #else:
            #print("Token error for", username) # return error if token cannot be found
        return self.fetched_auth
    
    def oath_authenticator(self,client_id,secret,redirect,scope,path='.spotipyoauthcache'):
        self.sp_oauth = oauth2.SpotifyOAuth(client_id,secret,redirect,scope)
        return self.sp_oauth
        

class Spotify_Scrape:

    test_artist = 'Flume' # test search string
    count = -1 # counter used for loops
    artist_names = [] # list stores followed artists
    artist_URI = [] # Unique identifier for artists in spotify API
    album_URI = [] # Unique identifier for albums in spotify API
    master_album = [] # master list of albums
    album_data = [] # holds temp album data information for storage in master list
    master_tracks = [] # master list of tracks
    playlist_names = [] # stores playlist names of user
    fixed_list = False # Restricts playlist to 100 songs

    def __init__(self, user_token):
        self.sp = spotipy.Spotify(auth=user_token)
        self.follows = self.sp.current_user_followed_artists(50) # pulls list of artists following
        self.num_artists = len(self.follows["artists"]["items"])
        self.playlist_id = self.checkPlaylists() # Spotify playlist ID to add tracks to
    
    def __str__(self):
        return str(self.__class__)

    def testSearch(self): # return test artist dictionary
        self.results = self.sp.search(q='artist:' + self.test_artist, type='artist')
        return self.results["artists"]["items"][0]

    def debugger(self, variant): # returns followed artists to identify artist dictionary labels
        if variant == 'artist':
            return self.follows["artists"]["items"][0] # delete 0 for all artists
        if variant == 'album':
            self.artistURIs()
            self.count = 0 # reset counter
            for occurrence in range(self.num_artists):
                self.entry = self.artist_URI[occurrence]
                self.artist_albums = self.sp.artist_albums(self.entry, album_type='album', limit='50')
                if occurrence == 4:
                    try:
                        for unique_album in range(len(self.artist_albums["items"])):
                            self.master_album.append(self.artist_albums["items"][unique_album]['release_date']) # add ['release_date'] to test release date pull
                    except IndexError:
                        continue
                elif occurrence == 5:
                    break
                else:
                    continue
            return self.master_album

    def pullArtists(self): # returns a list of every artist you follow
        self.count = -1 # reset counter
        for artist in range(self.num_artists):
            self.count += 1
            self.artist_names.append(self.follows["artists"]["items"][self.count]["name"])
        self.artist_names.sort()
        return self.artist_names

    def artistURIs(self): # returns list of artist URIs
        self.count = -1 # reset counter
        # Fetch Artist URIs
        for artist in range(self.num_artists):
            self.count += 1
            self.uri = self.follows["artists"]["items"][self.count]["uri"]
            self.artist_URI.append(self.uri)
        return self.artist_URI

    def albumURIs(self):
        global time_ago
        self.artistURIs()
        self.count = -1 # reset counter
        # Fetch Album URIs
        for occurrence in range(self.num_artists):
            self.entry = self.artist_URI[occurrence]
            self.artist_albums = self.sp.artist_albums(self.entry, album_type='album', limit='50')
            try:
                for unique_album in range(len(self.artist_albums["items"])):
                    try:
                        self.date_entry = self.artist_albums["items"][unique_album]["release_date"]
                        self.conv_date = datetime.datetime.strptime(self.date_entry, '%Y-%m-%d').date()
                        #print(self.conv_date) # Prints dates of scraped releases
                    except ValueError:
                        self.date_entry = self.artist_albums["items"][unique_album]["release_date"]
                        self.conv_date = datetime.datetime.strptime(self.date_entry, '%Y').date()
                        #print(self.conv_date) # Prints date where only release found
                    if self.conv_date > time_ago: # If release date accepted, append to master list
                        self.album_data.append(self.artist_albums["items"][unique_album]["uri"])
                        self.album_data.append(self.artist_albums["items"][unique_album]["release_date"])
                        self.master_album.append(self.album_data)
                        self.album_data = []
                    else:
                        continue
            except IndexError:
                continue
        return self.master_album

    def albumTracks(self):
        self.albumURIs()
        for occurrence in range(len(self.master_album)):
            self.unique_album_uri = self.master_album[occurrence][0]
            self.album_tracks = self.sp.album_tracks(self.unique_album_uri)
            try:
                for unique_track in range(len(self.album_tracks["items"])):
                    self.master_tracks.append(self.album_tracks["items"][unique_track]["uri"])
            except IndexError:
                continue
        with open("Output.txt", "w", encoding="utf-8") as text_file:
            print(f"{self.master_tracks}", file=text_file)
        print("Done!")
        return self.master_tracks

    def playlistAdd(self):
        global username # Find correct user for playlist creation
        self.shuffled_ids = [] # Contains only 100 results of shuffled track ids
        self.sp.trace = False
        self.playlistRemove() # Remove all tracks from existing playlist
        self.track_ids = self.albumTracks()
        random.shuffle(self.track_ids) # Shuffle tracks
        if len(self.track_ids) > 100:
            print('More than 100 tracks found')
            self.number_of_lists = len(self.track_ids) // 100
            print('No. of lists required equals ' + str(self.number_of_lists) + '. Generating...')
            if self.fixed_list == True: # If user forces list to contain fixed amount of tracks
                for identifier in range(100): # Creates new list with only 100 returned results
                    self.shuffled_ids.append(self.track_ids[identifier])
                    self.result = sp.user_playlist_add_tracks(username, self.playlist_id, self.shuffled_ids)
            elif self.fixed_list == False: # If user wishes all tracks returned
                for list_no in range(self.number_of_lists): # Populates list iteratively to not beat spotify API limit
                    for identifier in range(100):
                        self.shuffled_ids.append(self.track_ids[identifier])
                    self.result = self.sp.user_playlist_add_tracks(username, self.playlist_id, self.shuffled_ids)
                    self.shuffled_ids = []
                    del self.track_ids[0:100]
                self.result = self.sp.user_playlist_add_tracks(username, self.playlist_id, self.track_ids)
        else:
            self.result = self.sp.user_playlist_add_tracks(username, self.playlist_id, self.track_ids)
        #print(self.track_ids) # Returns and prints list of track ids to add to playlist
        print(self.result)

    def playlistRemove(self):
        global username
        self.playlist_uris = [] # stores URIs of tracks in playlist to delete
        self.result = self.sp.user_playlist_tracks(username, self.playlist_id)
        for entry in range(len(self.result["items"])):
            self.playlist_uris.append(self.result["items"][entry]['track']['uri'])
        self.remove_all = self.sp.user_playlist_remove_all_occurrences_of_tracks(username, self.playlist_id, self.playlist_uris) # Remove all tracks from playlist
        # Rerun to be absolutely sure if more tracks found
        self.result = self.sp.user_playlist_tracks(username, self.playlist_id)
        if len(self.result["items"]) > 0:
            self.playlistRemove()

    def checkPlaylists(self):
        self.userInfo()
        self.result = self.sp.user_playlists(self.user_id)
        for entry in range(len(self.result["items"])):
            self.playlist_names.append(self.result["items"][entry]["name"])
        if 'SpotifyWebScraper' in self.playlist_names:
            x = self.playlist_names.index('SpotifyWebScraper')
            self.returned_playlist = self.result["items"][x]["uri"]
            self.returned_playlist = self.returned_playlist.replace("spotify:", "") # formats scraped uri into playlist identifier
            self.playlist_id = f'spotify:user:{self.user_id}:{self.returned_playlist}'
        else:
            self.playlistCreate()
            self.checkPlaylists()
        #print(self.playlist_id) # Prints playlist ID for debugging
        return self.playlist_id

    def userInfo(self):
        self.result = self.sp.current_user()
        self.user_id = self.result['id']
        return self.user_id

    def playlistCreate(self):
        self.userInfo()
        self.result = self.sp.user_playlist_create(self.user_id,'SpotifyWebScraper')

# user_token_key = userAuthentication()
# user = Spotify_Scrape(user_token_key)

#print(user.testSearch()) # test search connection
#print(user.debugger('artist')) # test followed artists connection
#print(user.debugger('album'))
##print(user.pullArtists()) # prints list with followed artist names
##print(user.artistURIs()) # prints list of artist URIs
#print(user.albumURIs()) # returns list of artist URIs
#print(user.albumTracks())
#user.albumTracks() # Writes to text file a list of track URIs
# user.playlistAdd() # Adds tracks from within x release date
#user.playlistRemove() # Removes all tracks in specified playlist
#user.checkPlaylists()
#user.userInfo() # Fetches username from user id
#user.playlistCreate() # Autogenerates unpopulated playlist for correct formatting use in other elements of the application
