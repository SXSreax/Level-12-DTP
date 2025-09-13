from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash)
import sqlite3
import uuid
import werkzeug.security

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

        # Username: at least 2 letters or numbers, only letters and numbers
        if len(username) < 2 or not username.isalnum():
            flash(
                ('Username must be at least 2 letters or numbers, '
                 'and contain only letters and numbers.')
            )
            return redirect(url_for('signup.signup'))

        # Email: must contain @ before .
        if (
            '@' not in email or
            '.' not in email or
            email.index('@') > email.index('.')
        ):
            flash('Email must contain "@" before "."')
            return redirect(url_for('signup.signup'))

        # Password: at least 8 chars, must contain both letters and numbers,
        # only letters and numbers
        has_min_length = len(password) >= 8
        is_alphanumeric = password.isalnum()
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)

        if not (has_min_length
                and is_alphanumeric
                and has_letter
                and has_digit):
            flash(
                "Password must be at least 8 characters, "
                "contain both letters and numbers, "
                "and have no spaces or special characters."
            )
            return redirect(url_for('signup.signup'))

        hashed_pw = werkzeug.security.generate_password_hash(password)
        user_id = str(uuid.uuid4())
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, email)
            )
        if cursor.fetchone():
            flash('Username or email already exists.')
            return redirect(url_for('signup.signup'))
        cursor.execute(
            "INSERT INTO users (id, username, email, password) "
            "VALUES (?, ?, ?, ?)",
            (user_id, username, email, hashed_pw)
        )
        db.commit()
        db.close()
        flash('Sign up successful! Please log in.')
        return redirect(url_for('login.login'))
    return render_template('pages/signup.html')
