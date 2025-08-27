from flask import Blueprint, render_template, session
import sqlite3

hero_bp = Blueprint('hero', __name__)

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

@hero_bp.route('/hero/<id>')  # Page showing details of a hero, including their powers, abilities, and backstory
def hero(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, image_url, description FROM Hero WHERE id = ?", (id,))
    hero_details = cursor.fetchone()

    if hero_details:
        hero_name = hero_details[0]
        hero_avatar = hero_details[1]
        hero_description = hero_details[2]
    else:
        return render_template('404.html'), 404

    # Fetch abilities
    cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id,))
    abilities = cursor.fetchall()  # List of (name, description)

    # Fetch skins
    cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id,))
    skins = cursor.fetchall()  # List of (skin_name, skin_image_url)

    is_favorite = False
    user_id = session.get('user_id')
    if user_id:
        cursor.execute("SELECT 1 FROM Favorite WHERE user_id = ? AND hero_id = ?", (user_id, id))
        if cursor.fetchone():
            is_favorite = True
    db.close()
    return render_template(
        'hero.html',
        hero_name=hero_name,
        hero_avatar=hero_avatar,
        hero_description=hero_description,
        abilities=abilities,
        skins=skins,
        hero_id=id,
        is_favorite=is_favorite
    )