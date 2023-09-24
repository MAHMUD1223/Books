import json
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
with open('config.json', 'r') as c:
    data = json.load(c)
app.config['SQLALCHEMY_DATABASE_URI'] = data['uri']  # "sqlite:////dataßase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import forms, models, routes