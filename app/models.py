from app import db
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

