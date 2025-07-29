from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib

login_bp = Blueprint('login', __name__)

def get_db(): # getting the database connection
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_bp.route('/login', methods=['GET', 'POST'])  #page for user login, including a form for entering username and password
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
        user = cursor.fetchone()
        db.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!')
            return redirect(url_for('home.home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login.login'))
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login.login'))