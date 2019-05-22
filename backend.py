# import modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import codecs
import datetime
import random

# filter dates
today = datetime.date.today()
time_ago = today - datetime.timedelta(days=365)
print('Filtering from ' + str(time_ago))

# app credentials
cid ="244ce08ff106437f8e7565c2e796f4e3" 
secret = "6e652d745f094973a50ef8204b953828"
username = ""
redirect_url = "http://localhost:8888/callback/"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = """
user-read-recently-played user-top-read user-library-modify user-library-read playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-read-email user-read-birthdate user-read-private
user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-follow-read user-follow-modify
"""
token = util.prompt_for_user_token(username, scope, cid, secret, redirect_url)
if token:
    sp = spotipy.Spotify(auth=token) # try authentication
else:
    print("Token error for", username) # return error if token cannot be found

class Spotify_Scrape:

    test_artist = 'Flume' # test search string
    count = -1 # counter used for loops
    artist_names = [] # list stores followed artists
    artist_URI = [] # Unique identifier for artists in spotify API
    album_URI = [] # Unique identifier for albums in spotify API
    master_album = [] # master list of albums
    album_data = [] # holds temp album data information for storage in master list
    master_tracks = [] # master list of tracks
    playlist_uris = [] # stores URIs of tracks in playlist to delete
    playlist_id = 'spotify:user:alex_lossberg:playlist:2SxxmrnlUH2n37hyNUC6O6' # Spotify playlist ID to add to

    def __init__(self, user_token):
        self.sp = spotipy.Spotify(auth=user_token)
        self.follows = sp.current_user_followed_artists(50) # pulls list of artists following
        self.num_artists = len(self.follows["artists"]["items"])
    
    def __str__(self):
        return str(self.__class__)

    def testSearch(self): # return test artist dictionary
        self.results = sp.search(q='artist:' + self.test_artist, type='artist')
        return self.results["artists"]["items"][0]

    def debugger(self, variant): # returns followed artists to identify artist dictionary labels
        if variant == 'artist':
            return self.follows["artists"]["items"][0] # delete 0 for all artists
        if variant == 'album':
            self.artistURIs()
            self.count = 0 # reset counter
            for occurrence in range(self.num_artists):
                self.entry = self.artist_URI[occurrence]
                self.artist_albums = sp.artist_albums(self.entry, album_type='album', limit='50')
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
            self.artist_albums = sp.artist_albums(self.entry, album_type='album', limit='50')
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
            self.album_tracks = sp.album_tracks(self.unique_album_uri)
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
        sp.trace = False
        self.playlistRemove() # Remove all tracks from existing playlist
        self.track_ids = self.albumTracks()
        if len(self.track_ids) > 100:
            print('Error: More than 100 tracks found')
            random.shuffle(self.track_ids)
            #print(self.track_ids)
            for identifier in range(100): # Creates new list with only 100 returned results
                self.shuffled_ids.append(self.track_ids[identifier])
            self.result = sp.user_playlist_add_tracks(username, self.playlist_id, self.shuffled_ids)
        else:
            random.shuffle(self.track_ids)
            self.result = sp.user_playlist_add_tracks(username, self.playlist_id, self.track_ids)
        #print(self.track_ids) # Returns and prints list of track ids to add to playlist
        print(self.result)

    def playlistRemove(self):
        global username
        self.result = sp.user_playlist(username, self.playlist_id)
        for entry in range(len(self.result["tracks"]["items"])):
            self.playlist_uris.append(self.result["tracks"]["items"][entry]['track']['uri'])
        self.remove_all = sp.user_playlist_remove_all_occurrences_of_tracks(username, self.playlist_id, self.playlist_uris) # Remove all tracks from playlist

user = Spotify_Scrape(token)

#print(user.testSearch()) # test search connection
#print(user.debugger('artist')) # test followed artists connection
#print(user.debugger('album'))
##print(user.pullArtists()) # prints list with followed artist names
##print(user.artistURIs()) # prints list of artist URIs
#print(user.albumURIs()) # returns list of artist URIs
#print(user.albumTracks())
#user.albumTracks() # Writes to text file a list of track URIs
user.playlistAdd() # Adds tracks from within x release date
#user.playlistRemove()
