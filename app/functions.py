def process_search(query, db):
    cursor = db.cursor()

    # Check if the query is a number (assumes search by year)
    if query.isdigit():
        cursor.execute('SELECT * FROM movies WHERE release_year = %s', (query,))
        results = cursor.fetchall()

    else:
        # Search by exact movie title
        cursor.execute('SELECT * FROM movies WHERE title = %s', (query,))
        results = cursor.fetchall()

        # If no title matches, search by genre
        if not results:
            cursor.execute("""
                SELECT m.* FROM movies m
                JOIN movie_genres mg ON m.movie_id = mg.movie_id
                JOIN genres g ON mg.genre_id = g.genre_id
                WHERE g.genre_name = %s
            """, (query,))
            results = cursor.fetchall()

    return results