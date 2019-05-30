# from spswi.main.controllers import days_ago

# import modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from spotipy import oauth2
import codecs
import datetime
import random
import os
username = ""



class userAuthentication:

    def fetch_user_auth(self):
        # app credentials
        self.cid ="244ce08ff106437f8e7565c2e796f4e3" 
        self.secret = "6e652d745f094973a50ef8204b953828"
        self.username = ""
        self.redirect_url = "http://10.0.0.6:5000/"
        self.scope = 'user-read-recently-played user-top-read user-library-modify user-library-read playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-read-email user-read-birthdate user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-follow-read user-follow-modify'
        self.fetched_auth = self.oath_authenticator(self.cid,self.secret,self.redirect_url,self.scope)
        return self.fetched_auth
    
    def oath_authenticator(self,client_id,secret,redirect,scope,path='.spotipyoauthcache'):
        self.sp_oauth = oauth2.SpotifyOAuth(client_id,secret,redirect,scope=scope)
        return self.sp_oauth
        

class Spotify_Scrape:

    def __init__(self, user_token):
        #print("user token = " + str(user_token))
        self.sp = spotipy.Spotify(auth=user_token['access_token'])
        
    def testSearch(self):
        self.results = self.sp.search(q='artist:' + "Flume", type='artist')
        return self.results["artists"]["items"][0]

    def pullArtists(self):
        self.artist_names = []
        self.follows = self.sp.current_user_followed_artists(50)
        self.num_artists = len(self.follows["artists"]["items"])
        for artist in range(self.num_artists):
            self.artist_names.append(self.follows["artists"]["items"][artist]["name"])
        self.artist_names.sort()
        return self.artist_names
    
    def userInfo(self):
        self.result = self.sp.current_user()
        return self.result['id']

    def checkPlaylists(self):
        self.playlist_names = []
        self.user = self.userInfo()
        self.result = self.sp.user_playlists(self.user)
        #print(self.result["items"])
        for entry in range(len(self.result["items"])):
            self.playlist_names.append(self.result["items"][entry]["name"])
        if 'SpotifyWebScraper' in self.playlist_names:
            x = self.playlist_names.index('SpotifyWebScraper')
            self.returned_playlist = self.result["items"][x]["uri"]
            self.returned_playlist = self.returned_playlist.replace("spotify:", "") # formats scraped uri into playlist identifier
            self.playlist_id = f'spotify:user:{self.user}:{self.returned_playlist}'
        else:
            self.generate = self.sp.user_playlist_create(self.user,'SpotifyWebScraper') # Generate new playlist
            self.checkPlaylists()
        #print('playlist id = ' + self.playlist_id) # Prints playlist ID for debugging
        return self.playlist_id

    def uriArtist(self):
        self.artist_uris = []
        self.follows = self.sp.current_user_followed_artists(50)
        self.num_artists = len(self.follows["artists"]["items"])
        for artist in range(self.num_artists):
            self.artist_uris.append(self.follows["artists"]["items"][artist]["uri"])
        return self.artist_uris

    def uriAlbums(self,artist_uri,days_ago):
        print(days_ago)

        today = datetime.date.today()
        time_ago = today - datetime.timedelta(days=265)
        print('Filtering from ' + str(time_ago))

        self.master_album = []
        self.album_data = []
        for x in range(len(artist_uri)):
            self.entry = artist_uri[x]
            self.artist_albums = self.sp.artist_albums(self.entry, album_type='album', limit='50')
            try:
                for unique_album in range(len(self.artist_albums["items"])):
                    try:
                        self.date_entry = self.artist_albums["items"][unique_album]["release_date"]
                        self.conv_date = datetime.datetime.strptime(self.date_entry, '%Y-%m-%d').date()
                        
                    except ValueError:
                        self.date_entry = self.artist_albums["items"][unique_album]["release_date"]
                        self.conv_date = datetime.datetime.strptime(self.date_entry, '%Y').date()
                        #print(self.conv_date) # Prints date where only release found
                    if self.conv_date > time_ago: # If release date accepted, append to master list
                        # print(self.conv_date) # Prints dates of scraped releases
                        # print(days_ago)
                        self.album_data.append(self.artist_albums["items"][unique_album]["uri"])
                        self.album_data.append(self.artist_albums["items"][unique_album]["release_date"])
                        self.master_album.append(self.album_data)
                        self.album_data = []
                    else:
                        continue
            except IndexError:
                continue
        return self.master_album

    def uriTracks(self,album_uri):
        self.master_tracks = []
        for x in range(len(album_uri)):
            self.unique_album_uri = album_uri[x][0]
            self.album_tracks = self.sp.album_tracks(self.unique_album_uri)
            try:
                for unique_track in range(len(self.album_tracks["items"])):
                    self.master_tracks.append(self.album_tracks["items"][unique_track]["uri"])
            except IndexError:
                continue
        with open("Output.txt", "w", encoding="utf-8") as text_file:
            print(f"{self.master_tracks}", file=text_file)
        print("Exported Album Tracks!")
        return self.master_tracks

    def addPlaylist(self,track_uri,playlist):
        self.sp.trace = False
        self.user = self.userInfo()
        self.shuffled_ids = []
        random.shuffle(track_uri)
        if len(track_uri) > 100:
            for x in range(100): # Creates new list with only 100 returned results
                self.shuffled_ids.append(track_uri[x])
            self.result = self.sp.user_playlist_add_tracks(self.user, playlist, self.shuffled_ids)
            self.shuffled_ids = []
        else:
            self.result = self.sp.user_playlist_add_tracks(self.user, playlist, track_uri)

