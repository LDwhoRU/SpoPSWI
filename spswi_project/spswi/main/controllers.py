from flask import Blueprint, render_template, request
#from spswi.backend import pullArtists
from .functions import *

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Time period variables
day = 1
month = 30
year = 365

@main.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		frequency_input = 1
		frequncy_select = 'Days'
		days_ago = 1
		days_ago_select = 'Months'

		frequencyMultipler(frequency)
		##frequencyMultipler(days_ago)

		print(frequency)

#		try:
#			frequency_input = int(request.form['frequency_input'])
#			print(frequency_input)
#		except:
#			pass
#
#		try:
#			frequency_select = str(request.form['frequency_select'])
#			print(frequency_select)
#		except:
#			pass

		

		# if 'frequency' in request.form:
		# if 'days_ago' in request.form:
		#	  pass

	return render_template('primary.html',)# pull_artist = pullArtists())

