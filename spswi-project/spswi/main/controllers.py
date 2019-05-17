from flask import Blueprint, render_template
from spswi.main.backend import pullArtists

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('primary.html', pull_artist = 'test')
