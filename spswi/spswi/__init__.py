from flask import Flask, render_template
from spswi.main.controllers import main#, days_ago
# from spswi.main.backend import *


app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
