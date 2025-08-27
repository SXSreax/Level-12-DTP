from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

compare_bp = Blueprint('compare', __name__)

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

@compare_bp.route('/compare', methods=['GET', 'POST'])
def compare_select():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM Hero")
        heroes = cursor.fetchall()

    if request.method == 'POST':
        id1 = request.form.get('hero1')
        id2 = request.form.get('hero2')
        return redirect(url_for('compare.compare_result', id1=id1, id2=id2))
    return render_template('compare_select.html', heroes=heroes)

@compare_bp.route('/compare/<id1>/<id2>')
def compare_result(id1, id2):
    with get_db() as db:
        cursor = db.cursor()
        # Fetch hero 1 details
        cursor.execute("SELECT name, image_url, description FROM Hero WHERE id = ?", (id1,))
        h1 = cursor.fetchone()
        cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id1,))
        h1_abilities = cursor.fetchall()
        cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id1,))
        h1_skins = cursor.fetchall()

        # Fetch hero 2 details
        cursor.execute("SELECT name, image_url, description FROM Hero WHERE id = ?", (id2,))
        h2 = cursor.fetchone()
        cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id2,))
        h2_abilities = cursor.fetchall()
        cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id2,))
        h2_skins = cursor.fetchall()

    # If either hero is missing, show error page
    if h1 is None or h2 is None:
        return render_template('404.html', message="One or both heroes not found!"), 404

    hero1 = {
        "name": h1['name'], "image_url": h1['image_url'], "description": h1['description'],
        "abilities": h1_abilities, "skins": h1_skins
    }
    hero2 = {
        "name": h2['name'], "image_url": h2['image_url'], "description": h2['description'],
        "abilities": h2_abilities, "skins": h2_skins
    }
    return render_template('compare.html', hero1=hero1, hero2=hero2)