from flask import Blueprint, render_template, redirect, url_for, request, session, flash
import sqlite3

favorite_bp = Blueprint('favorite', __name__)

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

@favorite_bp.route('/favorite')  # page showing user's favorite heroes, allowing them to add or remove heroes from their favorites list
def favorite():
    username = session.get('username')
    if username:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            user_id = user[0]
            cursor.execute("SELECT hero_id FROM Favorite WHERE user_id = ?", (user_id,))
            favorite_hero_ids = cursor.fetchall()
            # Fetch hero details for each favorite hero
            favorite_heroes = []
            for hero_row in favorite_hero_ids:
                hero_id = hero_row[0]
                cursor.execute("SELECT id, name, image_url FROM Hero WHERE id = ?", (hero_id,))
                hero = cursor.fetchone()
                if hero:
                    favorite_heroes.append(hero)  # (id, name, image_url)
            db.close()
            return render_template('favorite.html', favorite_heroes=favorite_heroes)
        db.close()
    else:
        return redirect(url_for('login.login'))

@favorite_bp.route('/add_favorite/<int:hero_id>', methods=['POST'])
def add_favorite(hero_id):
    if 'user_id' not in session:
        flash('You must be logged in to add favorites.')
        return redirect(url_for('login.login'))
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Favorite WHERE user_id = ? AND hero_id = ?", (user_id, hero_id))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Favorite (user_id, hero_id) VALUES (?, ?)", (user_id, hero_id))
        db.commit()
        flash('Hero added to favorites!')
    else:
        flash('Hero is already in your favorites.')
    db.close()
    return redirect(url_for('hero.hero', id=hero_id))

@favorite_bp.route('/hero/<id>')
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
        return "Hero not found", 404

    cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id,))
    abilities = cursor.fetchall()

    cursor.execute("SELECT skin_name, image_url FROM Skins WHERE hero_id = ?", (id,))
    skins = cursor.fetchall()

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