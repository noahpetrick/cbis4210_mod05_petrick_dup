from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

movies = Blueprint('movies', __name__)

@movies.route('/movies', methods=['GET', 'POST'])
def movie():
    db = get_db()
    cursor = db.cursor()

    # Fetch all genres from the database
    cursor.execute('SELECT * FROM genres')
    genres = cursor.fetchall()

    if request.method == 'POST':
        title = request.form.get('title')
        release_year = request.form.get('release_year')
        selected_genres = request.form.getlist('genres')  # This will get the list of selected genre IDs

        if title and release_year:
            cursor.execute('INSERT INTO movies (title, release_year) VALUES (%s, %s)', (title, release_year))
            db.commit()

            # Get the movie_id of the newly inserted movie
            movie_id = cursor.lastrowid

            # Insert movie-genre associations into the movie_genres table
            for genre_id in selected_genres:
                cursor.execute('INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)', (movie_id, genre_id))
            db.commit()

            flash('New movie added successfully!', 'success')
            return redirect(url_for('movies.movie'))
        else:
            flash('Please provide both title and release year.', 'warning')

    cursor.execute('SELECT * FROM movies')
    movies_list = cursor.fetchall()
    return render_template('movies.html', movies=movies_list, genres=genres)

@movies.route('/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(movie_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch all genres from the database
    cursor.execute('SELECT * FROM genres')
    genres = cursor.fetchall()

    if request.method == 'POST':
        title = request.form.get('title')
        release_year = request.form.get('release_year')
        selected_genres = request.form.getlist('genres')  # Get the list of selected genre IDs

        cursor.execute('UPDATE movies SET title = %s, release_year = %s WHERE movie_id = %s', (title, release_year, movie_id))
        db.commit()

        # Clear existing movie-genre associations
        cursor.execute('DELETE FROM movie_genres WHERE movie_id = %s', (movie_id,))
        db.commit()

        # Insert new movie-genre associations
        for genre_id in selected_genres:
            cursor.execute('INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)', (movie_id, genre_id))
        db.commit()

        flash('Movie updated successfully!', 'success')
        return redirect(url_for('movies.movie'))

    cursor.execute('SELECT * FROM movies WHERE movie_id = %s', (movie_id,))
    movie = cursor.fetchone()

    # Fetch the genres that are associated with the movie
    cursor.execute('SELECT genre_id FROM movie_genres WHERE movie_id = %s', (movie_id,))
    current_genres = cursor.fetchall()
    current_genre_ids = [genre['genre_id'] for genre in current_genres]

    return render_template('update_movie.html', movie=movie, genres=genres, current_genre_ids=current_genre_ids)

@movies.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM movie_genres WHERE movie_id = %s', (movie_id,))
    db.commit()

    cursor.execute('DELETE FROM movies WHERE movie_id = %s', (movie_id,))
    db.commit()

    flash('Movie deleted successfully!', 'danger')
    return redirect(url_for('movies.movie'))