from flask import Flask, render_template
from spswi.main.controllers import main
import backend

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
