
from datetime import datetime
from .extensions import db



# db = SQLAlchemy()

class User(db.Model):
    
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(100))
    pic = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    # posts = db.relationship('Post', backref='author', lazy=True)
    # books = db.relationship('Book', backref='book_author', lazy=True)
        

class Book(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    # user = db.relationship('User', backref='user_books')


class Post(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    upvote = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    country = db.Column(db.String(100), nullable=False, default='Unknown')
    # author = db.relationship('User', backref='posts', lazy=True)
    # timestamp = db.Column(db.DateTime, default=datetime.utcnow) 
