from flask import Blueprint, render_template, request
import sqlite3

heroes_bp = Blueprint('heroes', __name__)

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

@heroes_bp.route('/heroes', methods=['GET', 'POST'])
def heroes():
    db = get_db()
    cursor = db.cursor()

    # Get all unique types for filter dropdown
    cursor.execute("SELECT DISTINCT types FROM Hero")
    types = [row['types'] for row in cursor.fetchall()]

    # Get search and filter values
    search_query = request.args.get('search', '').strip()
    filter_type = request.args.get('types', '')

    # Build query
    query = "SELECT id, image_url FROM Hero WHERE 1=1"
    params = []

    if search_query:
        query += " AND name LIKE ?"
        params.append(f"%{search_query}%")
    if filter_type:
        query += " AND types = ?"
        params.append(filter_type)

    cursor.execute(query, params)
    heroes = cursor.fetchall()
    db.close()


    return render_template('heroes.html', heroes=heroes, types=types, search_query=search_query, filter_type=filter_type)