from flask import Blueprint, render_template, request
from spswi.backend import pullArtists

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'login' in request.form:
            pass
        if 'search_artist' in request.form:
            pass
        if 'followed_artist' in request.form:
            print('working')
            pullArtists()

    return render_template('primary.html',)# pull_artist = pullArtists())

