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
		frequency_input = 30
		frequncy_select = 'Minutes'
		days_ago = 1
		days_ago_select = 'Months'

		if request.form['apply_settings'] == 'Apply Settings':
			try:
				frequency_input = int(request.form['frequency_input'])
				print(frequency_input)
			except:
				pass

			try:
				frequency_select = str(request.form['frequency_select'])
				print(frequency_select)
			except:
				pass

			try:
				days_ago_input = int(request.form['days_ago_input'])
				print(days_ago_input)
			except:
				pass

			try:
				days_ago_select = int(request.form['days_ago_select'])
				print(days_ago_select)
			except:
				pass

	return render_template('primary.html', frequency_input=frequency_input, frequency_select=frequency_select)# pull_artist = pullArtists())

