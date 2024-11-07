from flask import Blueprint, render_template, request, flash
from app.db_connect import get_db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    db = get_db()
    cursor = db.cursor()
    results = None  # Initialize results as None to handle no search case

    if request.method == 'POST':
        query = request.form.get('query')

        if query:
            # Check if the input is a number (assuming this is a search by year)
            if query.isdigit():
                cursor.execute('SELECT * FROM movies WHERE release_year = %s', (query,))
                results = cursor.fetchall()
                flash(f'Movies from the year {query}', 'info')

            else:
                # First try searching by exact movie title
                cursor.execute('SELECT * FROM movies WHERE title = %s', (query,))
                results = cursor.fetchall()

                if not results:
                    # If no title matches, try searching by genre
                    cursor.execute("""
                        SELECT m.* FROM movies m
                        JOIN movie_genres mg ON m.movie_id = mg.movie_id
                        JOIN genres g ON mg.genre_id = g.genre_id
                        WHERE g.genre_name = %s
                    """, (query,))
                    results = cursor.fetchall()

                # Set a message if results were found for genre or title
                if results:
                    flash(f'Results for "{query}":', 'success')
                else:
                    flash(f'No movies found for "{query}".', 'warning')

    return render_template('search.html', results=results)
