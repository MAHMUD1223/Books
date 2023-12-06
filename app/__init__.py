import secrets

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB example limit
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import forms, models, routes
