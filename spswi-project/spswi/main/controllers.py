from flask import Blueprint, render_template
#from spswi.main.backend import pullArtists

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('primary.html',)# pull_artist = pullArtists())

if request.method == 'POST':
    if request.form['submit_button'] == 'Do Something':
        pass # do something
    elif request.form['submit_button'] == 'Do Something Else':
        pass # do something else
    else:
        pass # unknown
