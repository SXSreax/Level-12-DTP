from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash
)
import sqlite3

favorite_bp = Blueprint('favorite', __name__)


def get_db():
    # Creates a database connection with row access
    # by column name for easier data handling
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


@favorite_bp.route('/favorite')
def favorite():
    """
    Displays the user's favorite heroes.

    Inputs:
        None directly; uses session to identify the user.

    Processing:
        - Checks if the user is logged in.
        - Retrieves the user's favorite hero IDs from the database.
        - Fetches details for each favorite hero.

    Outputs:
        Renders the favorite.html template with the user's favorite heroes.
        Redirects to login if not authenticated.
    """
    username = session.get('username')
    if username:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            user_id = user[0]
            # Gets all hero IDs the user has marked
            # as favorite for personalized display
            cursor.execute(
                "SELECT hero_id FROM Favorite WHERE user_id = ?",
                (user_id,)
            )
            favorite_hero_ids = cursor.fetchall()
            favorite_heroes = []
            # For each favorite hero, fetch details to show images/names
            for hero_row in favorite_hero_ids:
                hero_id = hero_row[0]
                cursor.execute(
                    "SELECT id, name, image_url FROM Hero WHERE id = ?",
                    (hero_id,)
                )
                hero = cursor.fetchone()
                if hero:
                    favorite_heroes.append(hero)  # (id, name, image_url)
            db.close()
            return render_template(
                'pages/favorite.html',
                favorite_heroes=favorite_heroes
            )
        db.close()
    else:
        # Redirects unauthenticated users to login
        # to protect user-specific data
        return redirect(url_for('login.login'))


@favorite_bp.route('/add_favorite/<int:hero_id>', methods=['POST'])
def add_favorite(hero_id):
    """
    Adds a hero to the user's favorites.

    Inputs:
        hero_id: The ID of the hero to add (from URL).
        Uses session to identify the user.

    Processing:
        - Checks if the user is logged in.
        - Prevents duplicate favorites by checking if already added.
        - Inserts the hero into the user's favorites if not present.

    Outputs:
        Redirects to the hero's page with a flash message indicating result.
    """
    if 'user_id' not in session:
        flash('You must be logged in to add favorites.')
        return redirect(url_for('login.login'))
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    # Ensures a hero isn't added twice to the user's favorites
    cursor.execute(
        "SELECT * FROM Favorite WHERE user_id = ? AND hero_id = ?",
        (user_id, hero_id)
    )
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Favorite (user_id, hero_id) VALUES (?, ?)",
                       (user_id, hero_id))
        db.commit()
        flash('Hero added to favorites!')
    else:
        flash('Hero is already in your favorites.')
    db.close()
    return redirect(url_for('hero.hero', id=hero_id))


@favorite_bp.route('/remove/<int:hero_id>', methods=['POST'])
def remove_favorite(hero_id):
    """
    Removes a hero from the user's favorites.

    Inputs:
        hero_id: The ID of the hero to remove (from URL).
        Uses session to identify the user.

    Processing:
        - Checks if the user is logged in.
        - Deletes the hero from the user's favorites in the database.

    Outputs:
        Redirects back to the previous page or the favorites page.
    """
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        cursor = db.cursor()
        # Removes the hero from favorites
        # for the current user to update their list
        cursor.execute("DELETE FROM Favorite WHERE user_id=? AND hero_id=?",
                       (user_id, hero_id))
        db.commit()
        db.close()
    return redirect(request.referrer or url_for('favorite.favorite'))
