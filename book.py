from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = create_engine('sqlite:///book.db', echo = True)
engine.connect()

Base = declarative_base()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    books = Book.query.all()
    return render_template('index.html', books = books)

@app.route("/add", methods=["POST"])
def addBook():
    title = request.form.get("title")
    author = request.form.get("author")
    body = request.form.get("body")
    pub_date = request.form.get("year")

    newBook = Book(title = title, author = author, body = body, pub_date = pub_date)
    db.session.add(newBook)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteBook(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/detail/<string:id>")
def detailBook(id):
    book = Book.query.filter_by(id=id).first()
    return render_template("detail.html", book = book)

@app.route("/edit/<string:id>", methods=["POST"])
def editBook(id):
    book = Book.query.filter_by(id=id).first()
    
    book.title = request.form.get("editTitle")
    book.author = request.form.get("editAuthor")
    book.body = request.form.get("editBody")
    book.pub_date = request.form.get("editYear")

    db.session.commit()
    return render_template("detail.html", book = book)

@app.route("/author/<string:author>")
def booksAuthor(author):
    booksAuthor = Book.query.filter_by(author = author)
    return render_template("author.html", booksAuthor = booksAuthor, author = author)

@app.route("/year/<string:pub_date>")
def booksYear(pub_date):
    booksYear = Book.query.filter_by(pub_date = pub_date)
    return render_template("year.html", booksYear = booksYear, pub_date = pub_date)

class Book(Base, db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.Integer)
    
Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)