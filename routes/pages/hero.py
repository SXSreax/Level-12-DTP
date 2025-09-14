from flask import Blueprint, render_template, session
import sqlite3

hero_bp = Blueprint('hero', __name__)


def get_db():
    # Creates a database connection with row access by column name
    # for easier data handling
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


@hero_bp.route('/hero/<id>')
def hero(id):
    """
    Displays details for a specific hero.

    Inputs:
        id: The hero's unique identifier from the URL.

    Processing:
        - Retrieves hero details from the database.
        - If hero not found, shows a 404 page.
        - Fetches abilities and skins for the hero.
        - Checks if the hero is in the user's favorites for personalized UI.

    Outputs:
        Renders the hero.html template with all hero data.
        Returns a 404 page if the hero does not exist.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT name, image_url, description FROM Hero WHERE id = ?",
        (id,)
    )
    hero_details = cursor.fetchone()

    if hero_details:
        hero_name = hero_details[0]
        hero_avatar = hero_details[1]
        hero_description = hero_details[2]
    else:
        # Shows a themed 404 page
        # if the hero ID is invalid or missing in the database
        return render_template('pages/404.html', message="Hero not found"), 404

    # Retrieves all abilities for the hero to display their powers
    cursor.execute(
        "SELECT ability_name, description FROM Abilities WHERE hero_id = ?",
        (id,)
    )
    abilities = cursor.fetchall()  # List of (name, description)

    # Retrieves all skins for the hero to show customization options
    cursor.execute(
        "SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?",
        (id,)
    )
    skins = cursor.fetchall()  # List of (skin_name, skin_image_url)

    is_favorite = False
    user_id = session.get('user_id')
    if user_id:
        # Checks if the current user has marked this hero as a favorite
        # for UI feedback
        cursor.execute(
            "SELECT 1 FROM Favorite WHERE user_id = ? AND hero_id = ?",
            (user_id, id)
        )
        if cursor.fetchone():
            is_favorite = True
    db.close()
    # Ensures hero_id is an integer for template logic
    hero_id = int(float(id))
    return render_template(
        'pages/hero.html',
        hero_name=hero_name,
        hero_avatar=hero_avatar,
        hero_description=hero_description,
        abilities=abilities,
        skins=skins,
        hero_id=hero_id,
        is_favorite=is_favorite
    )
