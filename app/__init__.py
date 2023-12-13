import secrets

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB example limit
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://MAHMUD1223:qZ5gMcIRDJl3@ep-plain-sky-804803-pooler.us-east-2.aws.neon.tech/book?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import forms, models, routes
