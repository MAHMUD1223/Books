import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB example limit
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.civqwbtmpkofhrolcfar:M7jpHdxtA)zgS:@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres" # 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
#app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'client_encoding': 'utf8'}
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models, forms