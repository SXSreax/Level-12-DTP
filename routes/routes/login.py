from flask import (
    Blueprint,
    render_template,
    request, redirect,
    url_for,
    flash,
    session
)
import sqlite3
import werkzeug.security

login_bp = Blueprint('login', __name__)


# getting the database connection
def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


# page for user login, including a form for entering username and password
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        db.close()
        if user and werkzeug.security.check_password_hash(
            user['password'], password
        ):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!')
            return redirect(url_for('home.home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login.login'))
    return render_template('pages/login.html')


@login_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login.login'))
