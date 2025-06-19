from flask import Blueprint, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/compare/<id1>/<id2>')  #page allowing users to compare two heroes side by side, showing their stats and abilities
def compare(id1, id2):
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

    hero1 = {
        "name": h1[0], "image_url": h1[1], "description": h1[2],
        "abilities": h1_abilities, "skins": h1_skins
    }
    hero2 = {
        "name": h2[0], "image_url": h2[1], "description": h2[2],
        "abilities": h2_abilities, "skins": h2_skins
    }
    return render_template('compare.html', hero1=hero1, hero2=hero2)