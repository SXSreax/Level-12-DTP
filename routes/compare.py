from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

compare_bp = Blueprint('compare', __name__)

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

@compare_bp.route('/compare', methods=['GET', 'POST'])
def compare_select():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM Hero")
    heroes = cursor.fetchall()
    db.close()

    if request.method == 'POST':
        id1 = request.form.get('hero1')
        id2 = request.form.get('hero2')
        return redirect(url_for('compare.compare_result', id1=id1, id2=id2))
    return render_template('compare_select.html', heroes=heroes)

@compare_bp.route('/compare/<id1>/<id2>')
def compare_result(id1, id2):
    db = get_db()
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
    db.close()

    hero1 = {
        "name": h1[0], "image_url": h1[1], "description": h1[2],
        "abilities": h1_abilities, "skins": h1_skins
    }
    hero2 = {
        "name": h2[0], "image_url": h2[1], "description": h2[2],
        "abilities": h2_abilities, "skins": h2_skins
    }
    return render_template('compare.html', hero1=hero1, hero2=hero2)