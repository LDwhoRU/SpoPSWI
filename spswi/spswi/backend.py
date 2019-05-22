# import modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import codecs
import operator
import datetime

# Import variables from flask
# from main.controllers import frequency

# app credentials
cid = "244ce08ff106437f8e7565c2e796f4e3"
secret = "6e652d745f094973a50ef8204b953828"
username = ""
redirect_url = "http://localhost:8888/callback/"
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = """
user-read-recently-played user-top-read user-library-modify user-library-read playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-read-email user-read-birthdate user-read-private
user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-follow-read user-follow-modify
"""
token = util.prompt_for_user_token(username, scope, cid, secret, redirect_url)
if token:
    sp = spotipy.Spotify(auth=token)  # try authentication
else:
    print("Token error for", username)  # return error if token cannot be found


class Spotify_Scrape:

    test_artist = 'Flume'  # test search string
    count = -1  # counter used for loops
    artist_names = []  # list stores followed artists
    artist_URI = []  # Unique identifier for artists in spotify API
    album_URI = []  # Unique identifier for albums in spotify API
    master_album = []  # master list of albums
    album_data = []  # holds temp album data information for storage in master list
    master_tracks = []  # master list of tracks
    track_data = []  # holds temp track data information

    def __init__(self, user_token):
        self.sp = spotipy.Spotify(auth=user_token)
        self.follows = sp.current_user_followed_artists(
            50)  # pulls list of artists following
        self.num_artists = len(self.follows["artists"]["items"])

    def __str__(self):
        return str(self.__class__)

    def timeController(self, days_ago):
        self.today = datetime.date.today()
        self.time_ago = self.today - datetime.timedelta(days=days_ago)
        self.time_ago = datetime.datetime.strptime(self.time_ago, "%d/%m/%Y")
        return self.time_ago

    def testSearch(self):  # return test artist dictionary
        self.results = sp.search(q='artist:' + self.test_artist, type='artist')
        return self.results["artists"]["items"][0]

    def debugger(self, variant):  # returns followed artists to identify artist dictionary labels
        if variant == 'artist':
            # delete 0 for all artists
            return self.follows["artists"]["items"][0]
        if variant == 'album':
            self.artistURIs()
            self.count = 0  # reset counter
            for occurrence in range(self.num_artists):
                self.entry = self.artist_URI[occurrence]
                self.artist_albums = sp.artist_albums(
                    self.entry, album_type='album', limit='50')
                if occurrence == 4:
                    try:
                        for unique_album in range(len(self.artist_albums["items"])):
                            # add ['release_date'] to test release date pull
                            self.master_album.append(
                                self.artist_albums["items"][unique_album]['release_date'])
                    except IndexError:
                        continue
                elif occurrence == 5:
                    break
                else:
                    continue
            return self.master_album

    def pullArtists(self):  # returns a list of every artist you follow
        self.count = -1  # reset counter
        for artist in range(self.num_artists):
            self.count += 1
            self.artist_names.append(
                self.follows["artists"]["items"][self.count]["name"])
        self.artist_names.sort()
        return self.artist_names

    def artistURIs(self):  # returns list of artist URIs
        self.count = -1  # reset counter
        # Fetch Artist URIs
        for artist in range(self.num_artists):
            self.count += 1
            self.uri = self.follows["artists"]["items"][self.count]["uri"]
            self.artist_URI.append(self.uri)
        return self.artist_URI

    def albumURIs(self, days_ago):
        self.artistURIs()
        self.count = -1  # reset counter
        self.timeController(days_ago)
        # Fetch Album URIs
        for occurrence in range(self.num_artists):
            self.entry = self.artist_URI[occurrence]
            self.artist_albums = sp.artist_albums(
                self.entry, album_type='album', limit='50')
            try:
                for unique_album in range(len(self.artist_albums["items"])):
                    self.date_con = self.artist_albums["items"][unique_album]["release_date"]
                    self.date_con = datetime.datetime.strptime(
                        self.date_con, "%d/%m/%Y")
                    if self.time_ago > self.date_con:
                        self.album_data.append(
                            self.artist_albums["items"][unique_album]["uri"])
                        self.album_data.append(
                            self.artist_albums["items"][unique_album]["release_date"])
                        self.master_album.append(self.album_data)
                    self.album_data = []
            except IndexError:
                continue
        return self.master_album

    def albumTracks(self, days_ago):
        self.albumURIs(days_ago)
        for occurrence in range(len(self.master_album)):
            self.unique_album_uri = self.master_album[occurrence][0]
            self.release_date = self.master_album[occurrence][1]
            self.album_tracks = sp.album_tracks(self.unique_album_uri)
            try:
                for unique_track in range(len(self.album_tracks["items"])):
                    self.track_data.append(
                        self.album_tracks["items"][unique_track]["uri"])
                    self.track_data.append(self.release_date)
                    self.master_tracks.append(self.track_data)
                    self.track_data = []
            except IndexError:
                continue
        self.master_tracks.sort(key=operator.itemgetter(1), reverse=True)
        with open("Output.txt", "w", encoding="utf-8") as text_file:
            print(f"{self.master_tracks}", file=text_file)
        print("Done!")
        return self.master_tracks


user = Spotify_Scrape(token)

# print(user.testSearch()) # test search connection
# print(user.debugger('artist')) # test followed artists connection
# print(user.debugger('album'))
# print(user.pullArtists()) # prints list with followed artist names
# print(user.artistURIs()) # prints list of artist URIs
# print(user.albumURIs(365)) # returns list of artist URIs
# print(user.albumTracks())
user.albumTracks(365)
# print(user.timeController(365))
