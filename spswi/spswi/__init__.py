from flask import Flask, render_template
from spswi.main.controllers import main
from spswi.admin.controllers import admin

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')