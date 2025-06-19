from flask import Blueprint, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()

favorite_bp = Blueprint('favorite', __name__)

@favorite_bp.route('/favorite')  #page showing user's favorite heroes, allowing them to add or remove heroes from their favorites list
def favorite():
    return render_template('favorite.html')