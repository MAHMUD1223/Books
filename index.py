import json
import secrets
import werkzeug
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError
from werkzeug.utils import secure_filename
from pdf2image import convert_from_bytes
import io
import base64

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
#color transparent
red="rgba()"

# Database Model

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    bookpdf = db.Column(db.LargeBinary, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name


class Assets_img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Asset {self.name}>'

    
# forms
class BookForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=16, message='Password must be between 8 and 16 characters long!')])
    bookpdf = FileField('bookpdf', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'PDFs only!')])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AssetForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=16, message='Password must be between 8 and 16 characters long!')])
    img = FileField('img', validators=[FileRequired(), FileAllowed({'png', 'jpg', 'jpeg'}, 'Images only!')])
    submit = SubmitField('Submit')

# Routes

@app.route('/urls')
@app.route('/_/')
def urls():
    import index
    alldir = dir(index)
    link = ""
    for i in alldir:
        try:
            link += f'<a href=\"{url_for(i)}\">{i}</a> <br>'
        except werkzeug.routing.exceptions.BuildError:
            pass
    return f'{link}'

@app.route('/home')
@app.route('/index')
@app.route('/index.html')
@app.route('/books')
@app.route('/')
def index():
    book=Books.query.all()
    return render_template('index.html', book=book)

@app.route('/assets/insert', methods=['GET', 'POST'])
def insert_asset():
    form = AssetForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data == data['pswd']:
            mimetype = form.img.data.mimetype
            img = form.img.data.read()
            filename = secure_filename(form.img.data.filename)
            new_img = Assets_img(name=filename, img=img, mimetype=mimetype)
            db.session.add(new_img)
            db.session.commit()
            flash('Img successfully added!', category='success')
            return redirect(url_for('view_assets'))
        else:
            flash('Hmmmmmm it seems like you entered somthing worng here', category="danger")
            return redirect(url_for('insert_asset'))
    return render_template('insert_asset.html', form=form)

@app.route('/assets/view')
def view_assets():
    asset = Assets_img.query.all()
    return render_template('view_assets.html', asset=asset)

@app.route('/assets/<int:id>')
def assets(id):
    asset = Assets_img.query.get_or_404(id)
    return Response(asset.img, mimetype=asset.mimetype)

@app.route('/book/insert', methods=['GET', 'POST'])
def insert_book():
    form = BookForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data == data['pswd']:
            bookpdf = form.bookpdf.data.read()
            new_book = Books(name=form.name.data, bookpdf=bookpdf, description=form.description.data)
            db.session.add(new_book)
            db.session.commit()
            flash('Book successfully added!', category='success')
            return redirect(url_for('index'))
        else:
            flash('Hmmmmmm, it seems like you entered something worng here', category="danger")
            return redirect(url_for('insert_book'))
    return render_template('insert_book.html', form=form)


@app.route('/book/<int:id>')
def book(id):
    pdf = Books.query.filter_by(id=id).first_or_404()
    pdf_data = pdf.bookpdf

    if pdf_data:
        images = convert_from_bytes(pdf_data, size=(800, None), dpi=200)
        
        # Convert the images to base64-encoded strings
        image_strings = []
        for image in images:
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            image_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_strings.append(image_string)

    return render_template('book.html', book=pdf, image=image_strings)


@app.route('/about')
def about():
    return render_template('about.html')
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__=="__main__":
    app.run(debug=True)

