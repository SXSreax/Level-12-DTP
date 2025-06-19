from flask import Blueprint, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()

heroes_bp = Blueprint('heroes', __name__)

@heroes_bp.route('/heroes')  #page showing all heros in the game, pictures, names, and basic details about them
def heroes():
    cursor.execute("SELECT id, image_url FROM Hero")
    heroes = cursor.fetchall()  # List of (id, image_url)
    return render_template('heroes.html', heroes=heroes)