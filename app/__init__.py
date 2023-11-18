import secrets
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
with open('config.json', 'r', encoding='utf-8') as c:
    data = json.load(c)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB example limit
app.config['SQLALCHEMY_DATABASE_URI'] = data['uri2']#'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models, forms