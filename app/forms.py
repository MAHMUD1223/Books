from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError

class BookForm(FlaskForm):
    book_name = StringField('name', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=16,
                message='Password must be between 8 and 16 characters long!')])
    bookpdf = FileField(
        'bookpdf', validators=[
            FileRequired(), FileAllowed(
                {'pdf'}, 'PDFs only!')])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('Submit')
