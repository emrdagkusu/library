from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from sqlalchemy import Column, Integer, MetaData, String, create_engine
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
engine = create_engine('sqlite:///book.db', echo = True)
engine.connect()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SECRET_KEY'] = 'hello_world'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route("/")
def index():
    form = LoginForm(request.form)
    if not current_user.is_authenticated:
        return render_template('login.html', form = form)
    else:
        books = Book.query.filter_by(userID = current_user.id)
        return render_template('index.html', books = books.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if not user:
            return render_template('login.html', form = form, error = 'User Not Found')  

        if not check_password_hash(user.password, request.form['password']) and not request.form['username'] == user.username:
            return render_template('login.html', form = form, error = 'Incorrect password or username')
        
        if check_password_hash(user.password, request.form['password']) and request.form['username'] == user.username:
            login_user(user)
            
        next = request.args.get('next')
        return redirect(next or url_for('index'))

    return render_template('login.html', form = form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return None

    return db.session.query(User).get(user_id)

@app.route('/signup')
def form():
    form = RegisterForm()
    return render_template('register.html', form = form)

@app.route("/register", methods =['POST', 'GET'])
def users():
    try:
        if request.method == 'POST':

            username = request.form.get('username')
            password = request.form.get('password')

            newUser = User(username = username, password = generate_password_hash(password, method='sha256'))
            db.session.add(newUser)
            db.session.commit()

            return redirect(url_for('index'))
    except:
        form = RegisterForm()
        return render_template("register.html", form = form, error="Username has already been taken.")

@app.route("/add", methods=["POST"])
@login_required
def addBook():
    title = request.form.get("title")
    author = request.form.get("author")
    body = request.form.get("body")
    pub_date = request.form.get("year")
    userID = current_user.id
    newBook = Book(title = title, author = author, body = body, pub_date = pub_date, userID = userID)
    db.session.add(newBook)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
@login_required
def deleteBook(id):
    book = Book.query.filter_by(id=id, userID = current_user.id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/detail/<string:id>")
@login_required
def detailBook(id):
    book = Book.query.filter_by(id=id, userID = current_user.id).first()
    return render_template("detail.html", book = book)

@app.route("/edit/<string:id>", methods=["POST"])
@login_required
def editBook(id):
    book = Book.query.filter_by(id=id, userID = current_user.id).first()
    
    book.title = request.form.get("editTitle")
    book.author = request.form.get("editAuthor")
    book.body = request.form.get("editBody")
    book.pub_date = request.form.get("editYear")

    db.session.commit()
    return render_template("detail.html", book = book)

@app.route("/author/<string:author>")
@login_required
def booksAuthor(author):
    booksAuthor = Book.query.filter_by(author = author, userID = current_user.id)
    return render_template("author.html", booksAuthor = booksAuthor, author = author)

@app.route("/year/<string:pub_date>")
@login_required
def booksYear(pub_date):
    booksYear = Book.query.filter_by(pub_date = pub_date, userID = current_user.id)
    return render_template("year.html", booksYear = booksYear, pub_date = pub_date)

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.Integer)
    userID = db.Column(db.Integer)


class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(32))
    
db.Model.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)