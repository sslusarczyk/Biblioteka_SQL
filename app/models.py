# app/models.py
from app import db
from datetime import datetime, timedelta

authors_books = db.Table('authors_books',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', secondary=authors_books, backref='authors', lazy='dynamic')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    borrowings = db.relationship('Borrowing', backref='book', lazy=True)

class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower_name = db.Column(db.String(100), nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)