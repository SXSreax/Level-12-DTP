import sqlite3
from flask import session

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

def inject_profile_image():
    profile_image_url = 'images/default.png'
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT profile_image FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        db.close()
        if user and user['profile_image']:
            profile_image_url = user['profile_image']
    return dict(profile_image_url=profile_image_url)