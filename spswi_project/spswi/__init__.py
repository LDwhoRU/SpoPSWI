from flask import Flask, render_template
from spswi.main.controllers import main
from spswi.main.functions import *

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
