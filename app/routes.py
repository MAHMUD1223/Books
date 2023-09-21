
import werkzeug
import fitz
import base64
import io
from app import app, db, data
from werkzeug.utils import secure_filename
from app.models import Books, Assets_img
from app.forms import BookForm, AssetForm
from flask import render_template, request, redirect, url_for, flash, Response



@app.route('/urls')
@app.route('/_/')
def urls():
    from app import routes as index
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

    """
    if pdf_data:
        images = convert_from_bytes(pdf_data, size=(800, None), dpi=200)
        
        # Convert the images to base64-encoded strings
        image_strings = []
        for image in images:
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            image_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_strings.append(image_string)

    return render_template('book.html', book=pdf, image=image_strings)"""
    if pdf_data:
        pdf_document = fitz.open(stream=io.BytesIO(pdf_data), filetype="pdf")
        num_pages = pdf_document.page_count

        page_images = []
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img_stream = io.BytesIO()
            #https://chat.openai.com/share/a7001588-73b1-4f88-bb48-1a80c1679bd6
            pix.save(img_stream, format="png")
            
            img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
            img_stream.close()
            
            page_images.append(img_base64)

    return render_template('book.html',book=pdf, image=page_images)



@app.route('/about')
def about():
    return render_template('about.html')
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

