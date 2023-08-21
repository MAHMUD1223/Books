import json
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError

app = Flask(__name__)
with open('config.json', 'r') as c:
    data = json.load(c)
app.config['SQLALCHEMY_DATABASE_URI'] = data['uri'] #"sqlite:////dataßase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Variables
ALLOWED_EXTENSIONS = {'pdf'}

# Database Model

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    bookpdf = db.Column(db.LargeBinary, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name
    
# forms
class BookForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    bookpdf = FileField('bookpdf', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'PDFs only!')])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Routes

@app.route('/')
def index():
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)

