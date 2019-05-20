from flask import Blueprint, render_template, request
#from spswi.backend import pullArtists

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Time period variables
day = 1
month = 30
year = 365

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        frequency = 1 * year
        days_ago = 1 * month

        try:
            frequency = int(request.form["frequency"])
            print(frequency)
        except:
            pass

        # if 'frequency' in request.form:
        # if 'days_ago' in request.form:
        #     pass

    return render_template('primary.html',)# pull_artist = pullArtists())

