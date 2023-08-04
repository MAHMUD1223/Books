import os
import random
import datetime as dt
# , get_flashed_messages
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import Email, EqualTo, Length, DataRequired, optional, ValidationError
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
from flask_mail import Mail, Message

app = Flask(__name__)

@app.route('/')
def index():
    return "hello from book"

if __name__=='__main__':
    app.run(debug=True, port=random.randint(5000, 9000))