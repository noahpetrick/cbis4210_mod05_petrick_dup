from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db
import pymysql.cursors

genres = Blueprint('genres', __name__)

@genres.route('/genres', methods=['GET', 'POST'])
def genre():
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)  # Use DictCursor for dictionary cursor

    if request.method == 'POST':
        genre_name = request.form.get('genre_name')

        if genre_name:
            cursor.execute('INSERT INTO genres (genre_name) VALUES (%s)', (genre_name,))
            db.commit()
            flash('New genre added successfully!', 'success')
            return redirect(url_for('genres.genre'))
        else:
            flash('Please provide a genre name.', 'warning')

    cursor.execute('SELECT * FROM genres')
    genres_list = cursor.fetchall()

    for genre in genres_list:
        cursor.execute('''SELECT m.movie_id, m.title, m.release_year
                          FROM movies m
                          JOIN movie_genres mg ON m.movie_id = mg.movie_id
                          WHERE mg.genre_id = %s''', (genre['genre_id'],))
        genre['movies'] = cursor.fetchall()

    return render_template('genres.html', genres=genres_list)

@genres.route('/update_genre/<int:genre_id>', methods=['GET', 'POST'])
def update_genre(genre_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        genre_name = request.form.get('genre_name')

        if genre_name:
            cursor.execute('UPDATE genres SET genre_name = %s WHERE genre_id = %s', (genre_name, genre_id))
            db.commit()

            flash('Genre updated successfully!', 'success')
            return redirect(url_for('genres.genre'))

        else:
            flash('Please provide a genre name.', 'warning')

    cursor.execute('SELECT * FROM genres WHERE genre_id = %s', (genre_id,))
    genre = cursor.fetchone()
    return render_template('update_genre.html', genre=genre)

@genres.route('/delete_genre/<int:genre_id>', methods=['POST'])
def delete_genre(genre_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM genres WHERE genre_id = %s', (genre_id,))
    db.commit()

    flash('Genre deleted successfully!', 'danger')
    return redirect(url_for('genres.genre'))