from flask import render_template, request, flash
from . import app  # Import the app instance from __init__.py
from app.db_connect import get_db
from app.functions import process_search  # Import the search processing function if you have one

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])  # Use '/about' for the search page and form submission
def search():
    db = get_db()  # Get the database connection
    results = None  # Initialize results as None to handle the case where there are no results

    if request.method == 'POST':
        query = request.form.get('query')  # Get the search query from the form
        if query:
            results = process_search(query, db)  # Process the query to get search results
            # Flash a message based on results
            if results:
                flash(f'Results for "{query}":', 'success')
            else:
                flash(f'No movies found for "{query}".', 'warning')

    return render_template('search.html', results=results)  # Render the search page with the results
