from . import db


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    book = db.Column(db.Text, nullable=False)
    page = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Book %r>' % self.book_name
        