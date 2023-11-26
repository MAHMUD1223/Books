import base64
import io
import os
import tempfile

import fitz  # it's from pymupdf
from flask import Response, flash, redirect, render_template, request, url_for

from . import app, backside, db
from .forms import BookForm
from .models import Books

backside.Backside()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/book/insert', methods=['GET', 'POST'])
def book_insert():
    form = BookForm()
    if request.method == "POST" and form.validate_on_submit() and form.password.data == "nopassword":
        book_name = form.book_name.data
        author = form.author.data
        pdf_data = form.bookpdf.data.read()
        description = form.description.data
        if pdf_data:
            pdf_document = fitz.open(stream=io.BytesIO(pdf_data), filetype="pdf")
            num_pages = pdf_document.page_count
            page_images = ""

            for page_num in range(num_pages):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    pix.save(temp_file.name)

                with open(temp_file.name, "rb") as image_file:
                    img_base64 = base64.b64encode(image_file.read()).decode('utf-8')

                os.remove(temp_file.name)

                page_images += f",{img_base64}"
        else:
            flash('something went worng try again', category="danger")
            return redirect(url_for('book_insert'))
        new_book = Books(book_name=book_name,
                         author=author,
                         description=description,
                         book=page_images[1:],
                         page=num_pages)
        db.session.add(new_book)
        db.session.commit()
        flash(f"Book:{book_name} added successfully", category="success")
        return redirect(url_for('book'))
    return render_template('book_insert.html', form=form)


@app.route('/book')
def book():
    books = Books.query.with_entities(Books.id, Books.book_name, Books.author).all()
    return render_template('book_index.html', books=books)


@app.route('/page/<id>/<page>')
def page(id, page):
    book_page = Books.query.filter_by(id=id).first_or_404().book.split(",")[int(page)]
    img_data = base64.b64decode(book_page)
    return Response(img_data, mimetype='image/png')


@app.route('/read/<id>')
def read(id):
    book = Books.query.filter_by(id=id).with_entities(Books.id ,Books.book_name, Books.author, Books.page).first_or_404()
    return render_template("read.html", book=book)
