from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

compare_bp = Blueprint('compare', __name__)


def get_db():
    """
    Return a connection to the Heroes.db SQLite database
    with row access by column name.
    This ensures consistent database access
    and easier row handling throughout the module.
    """
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


@compare_bp.route('/compare', methods=['GET', 'POST'])
def compare_select():
    """
    Hero comparison selection page.

    Inputs:
        - GET: None
        - POST: hero1 and hero2 IDs from form data

    Processing:
        - On GET: Fetch all heroes for selection.
        - On POST: If two heroes are selected,
        redirect to the comparison result page.
          Redirecting after POST avoids duplicate form submissions
          and keeps URLs meaningful.

    Outputs:
        - Renders the hero selection form (GET)
        - Redirects to the comparison result page (POST)
    """
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM Hero")
        heroes = cursor.fetchall()

    if request.method == 'POST':
        id1 = request.form.get('hero1')
        id2 = request.form.get('hero2')
        # Only redirect if both heroes are selected, ensuring valid comparison
        if id1 and id2:
            return redirect(url_for('compare.compare_result',
                                    id1=id1, id2=id2))
    return render_template('pages/compare_select.html', heroes=heroes)


@compare_bp.route('/compare/<id1>/<id2>')
def compare_result(id1, id2):
    """
    Detailed comparison between two heroes.

    Inputs:
        - id1, id2: Hero IDs from the URL

    Processing:
        - Fetches details, abilities, and skins for both heroes.
        - If either hero does not exist, renders a themed 404 page.
          This prevents errors if users manually enter invalid IDs.

    Outputs:
        - Renders the comparison page with both heroes' data
        - Renders a 404 page if either hero is missing
    """
    with get_db() as db:
        cursor = db.cursor()
        # Gather all relevant data for hero 1
        cursor.execute(
            "SELECT name, image_url, description FROM Hero WHERE id = ?",
            (id1,)
        )
        h1 = cursor.fetchone()
        cursor.execute(
            "SELECT ability_name, description FROM Abilities WHERE hero_id= ?",
            (id1,)
        )
        h1_abilities = cursor.fetchall()
        cursor.execute(
            "SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?",
            (id1,)
        )
        h1_skins = cursor.fetchall()

        # Gather all relevant data for hero 2
        cursor.execute(
            "SELECT name, image_url, description FROM Hero WHERE id = ?",
            (id2,)
        )
        h2 = cursor.fetchone()
        cursor.execute(
            "SELECT ability_name, description FROM Abilities WHERE hero_id= ?",
            (id2,)
        )
        h2_abilities = cursor.fetchall()
        cursor.execute(
            "SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?",
            (id2,)
        )
        h2_skins = cursor.fetchall()

    # If either hero is missing, show a themed error page to guide the user
    if h1 is None or h2 is None:
        return render_template(
            'pages/404.html',
            message="One or both heroes not found!"
        ), 404

    hero1 = {
        "name": h1['name'],
        "image_url": h1['image_url'],
        "description": h1['description'],
        "abilities": h1_abilities,
        "skins": h1_skins
    }
    hero2 = {
        "name": h2['name'],
        "image_url": h2['image_url'],
        "description": h2['description'],
        "abilities": h2_abilities,
        "skins": h2_skins
    }
    # Pass both hero dicts to the template for rendering the comparison
    return render_template('pages/compare.html', hero1=hero1, hero2=hero2)
