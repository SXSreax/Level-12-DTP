from flask import Blueprint, render_template, request
import sqlite3

heroes_bp = Blueprint('heroes', __name__)


def get_db():
    # Creates a database connection with row access by column name
    # for easier data handling
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


@heroes_bp.route('/heroes', methods=['GET', 'POST'])
def heroes():
    """
    Displays a list of heroes, with search and filter functionality.

    Inputs:
        - GET/POST request with optional 'search' and 'types' query parameters.

    Processing:
        - Retrieves all unique hero types for the filter dropdown.
        - Cleans the search query to avoid issues with special characters.
        - Builds a dynamic SQL query based on search and filter inputs.
        - Fetches matching heroes from the database.

    Outputs:
        Renders the heroes.html template with the filtered hero list,
        available types, and current search/filter values.
    """
    db = get_db()
    cursor = db.cursor()

    # Retrieves all unique hero types for the filter dropdown
    # so users can filter by type
    cursor.execute("SELECT DISTINCT types FROM Hero")
    types = [row['types'] for row in cursor.fetchall()]

    # Gets search and filter values from the request for dynamic filtering
    search_query = request.args.get('search', '').strip()
    filter_type = request.args.get('types', '')

    # Cleans the search query to improve matching and prevent SQL issues
    cleaned_search = ''.join([c.lower() for c in search_query if c.isalnum()])

    # Builds the base query for hero selection
    # using a normalized name for search
    query = """SELECT id,
        image_url,
        LOWER(REPLACE(name, '-', '')) as lname FROM Hero WHERE 1=1"""
    params = []

    # Adds search condition if user entered a query, so results are relevant
    if cleaned_search:
        query += " AND lname LIKE ?"
        params.append(f"%{cleaned_search}%")
    # Adds type filter if selected, so users can narrow results
    if filter_type:
        query += " AND types = ?"
        params.append(filter_type)

    cursor.execute(query, params)
    heroes = cursor.fetchall()
    db.close()

    # Renders the hero list page with all relevant data
    # for display and filtering
    return render_template(
        'pages/heroes.html',
        heroes=heroes,
        types=types,
        search_query=search_query,
        filter_type=filter_type
    )
