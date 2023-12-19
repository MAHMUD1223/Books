import secrets
import json

from flask import Flask
from flask_minify import minify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

with open('sj', 'r') as c:
    data = json.load(c)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB example limit
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book.sqlite"#data['in'][::-1]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
minify(app=app, html=True, js=True, cssless=True, static=True)

from . import forms, models, routes
