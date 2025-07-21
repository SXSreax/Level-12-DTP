from flask import Blueprint, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()

hero_bp = Blueprint('hero', __name__)

@hero_bp.route('/hero/<id>')  # Page showing details of a hero, including their powers, abilities, and backstory
def hero(id):
    # Fetch hero details
    cursor.execute("SELECT name, image_url, description FROM Hero WHERE id = ?", (id,))
    hero = cursor.fetchone()

    if not hero:
        return "Hero not found", 404

    hero_name = hero[0]
    hero_avatar = hero[1]
    hero_description = hero[2]

    # Fetch abilities
    cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id,))
    abilities = cursor.fetchall()  # List of (name, description)

    # Fetch skins
    cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id,))
    skins = cursor.fetchall()  # List of (skin_name, skin_image_url)

    print(hero_avatar)

    return render_template(
        'hero.html',
        hero_name=hero_name,
        hero_avatar=hero_avatar,
        hero_description=hero_description,
        abilities=abilities,
        skins=skins,
        hero_id=id  
    )