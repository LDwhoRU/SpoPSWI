from flask import Blueprint, render_template, request
#from spswi.main.backend import pullArtists

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('primary.html',)# pull_artist = pullArtists())

@main.route('/auth')
def auth():
    if request.method == "POST":
        auth = request.form
        from spswi.main.backend import pullArtists
        pullArtists()
