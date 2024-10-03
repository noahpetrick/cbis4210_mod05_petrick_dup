from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

books = Blueprint('books', __name__)


@books.route('/book', methods=['GET', 'POST'])
def book():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new runner
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        book_price = request.form['book_price']

        # Insert the new runner into the database
        cursor.execute('INSERT INTO books (book_name, book_author, book_price) VALUES (%s, %s, %s)', (book_name, book_author, book_price))
        db.commit()

        flash('New book added successfully!', 'success')
        return redirect(url_for('books.book'))

    # Handle GET request to display all runners
    cursor.execute('SELECT * FROM books')
    all_books = cursor.fetchall()
    return render_template('books.html', all_books=all_books)


@books.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the runner's details
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        book_price = request.form['book_price']

        cursor.execute('UPDATE books SET book_name = %s, book_author = %s, book_price = s% WHERE book_id = %s',
                       (book_name, book_author, book_price, book_id))
        db.commit()

        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.book'))

    # GET method: fetch runner's current data for pre-populating the form
    cursor.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
    book = cursor.fetchone()
    return render_template('update_book.html', book=book)


@books.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the runner
    cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
    db.commit()

    flash('Book deleted successfully!', 'danger')
    return redirect(url_for('books.book'))
