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

@favorite_bp.route('/remove/<int:hero_id>', methods=['POST'])
def remove_favorite(hero_id):
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Favorite WHERE user_id=? AND hero_id=?", (user_id, hero_id))
        db.commit()
        db.close()
    return redirect(request.referrer or url_for('favorite.favorite'))