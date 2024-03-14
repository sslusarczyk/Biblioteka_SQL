from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Author, Book, Borrowing

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author_id = request.form.get('author_id')
    if not title or not author_id:
        # Handle validation error
        return redirect(url_for('index'))

    author = Author.query.get(author_id)
    if not author:
        # Handle author not found
        return redirect(url_for('index'))

    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/borrow_book/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    borrower_name = request.form.get('borrower_name')
    if not borrower_name:
        # Handle validation error
        return redirect(url_for('index'))

    book = Book.query.get(book_id)
    if not book or not book.is_available:
        # Handle book not found or already borrowed
        return redirect(url_for('index'))

    existing_borrowing = Borrowing.query.filter_by(book_id=book_id, borrower_name=borrower_name).first()
    if existing_borrowing:
        # Handle book already borrowed by the same borrower
        return redirect(url_for('index'))

    borrowing = Borrowing(borrower_name=borrower_name, book=book)
    book.is_available = False
    db.session.add(borrowing)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/return_book/<int:borrowing_id>', methods=['POST'])
def return_book(borrowing_id):
    borrowing = Borrowing.query.get(borrowing_id)
    if not borrowing:
        # Handle borrowing not found
        return redirect(url_for('index'))

    book = borrowing.book
    if not book:
        # Handle book not found
        return redirect(url_for('index'))

    book.is_available = True
    db.session.delete(borrowing)
    db.session.commit()
    return redirect(url_for('index'))