spotifyPlaylistScraper
==================================

spotifyPlaylistScraper is a semi-automated tool designed for Linux and MacOS that allows users to populate a spotify playlist at
regular intervals. The script will fetch the entire discography of artists you follow and filter the returned results to only include
releases from a predefined period of time. Our handy flask companion tool can be used to manage the script, sign in to your spotify
account, and generate the playlist.

### Required dependencies

* Spotipy
* apscheduler
* Flask

##### Standalone version

For your convenience, included is a lightweight command-line version in the root folder, titled backend.py. The user class takes no specific parameters, but every method can be manually executed.

*IFB102 Submission Sem 1 2019*
