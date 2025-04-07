from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Add the relationship to link User to their reviews
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Book(db.Model):
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    publisher = db.Column(db.String(100))
    image = db.Column(db.String(200))

    # Add the relationship to link Book to its reviews
    reviews = db.relationship('Review', back_populates='book', cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isbn = db.Column(db.String, db.ForeignKey('book.isbn'), nullable=False)

    # Define relationships for Review
    user = db.relationship('User', back_populates='reviews')
    book = db.relationship('Book', back_populates='reviews')

    def __repr__(self):
        return f"<Review {self.text} - Rating: {self.rating}>"