from spswi.main.controllers import days_ago

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

# filter dates
today = datetime.date.today()
time_ago = today - datetime.timedelta(days=days_ago)
print('Filtering from ' + str(time_ago))

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
        print("user token = " + str(user_token))
        self.sp = spotipy.Spotify(auth=user_token['access_token'])
        
    def testSearch(self):
        self.results = self.sp.search(q='artist:' + "Flume", type='artist')
        return self.results["artists"]["items"][0]
