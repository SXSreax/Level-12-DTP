from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
import uuid  # Add this import

sign_up_bp = Blueprint('signup', __name__)

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

@sign_up_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        db = get_db()
        cursor = db.cursor()
        # Check if username or email exists
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            flash('Username or email already exists.')
            return redirect(url_for('signup.signup'))
        # Insert new user with user_id
        cursor.execute(
            "INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)",
            (user_id, username, email, hashed_pw)
        )
        db.commit()
        db.close()
        flash('Sign up successful! Please log in.')
        return redirect(url_for('login.login'))
    return render_template('signup.html')