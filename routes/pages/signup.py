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
    # Creates a database connection with row access by column name
    # for easier data handling
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


@sign_up_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles user registration.

    Inputs:
        - POST request with 'username', 'email', and 'password'
        from the signup form.

    Processing:
        - Validates username, email, and password for format and uniqueness.
        - Hashes the password for secure storage.
        - Inserts new user into the database if validation passes.
        - Provides feedback via flash messages.

    Outputs:
        - Redirects to login page on successful signup.
        - Redirects back to signup page with error message on failure.
        - Renders signup page for GET requests.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validates username for minimum length and allowed characters
        # prevent invalid accounts
        if len(username) < 2 or not username.isalnum():
            flash(
                ('Username must be at least 2 letters or numbers, '
                 'and contain only letters and numbers.')
            )
            return redirect(url_for('signup.signup'))

        # Checks email format to reduce user errors and ensure contactability
        if (
            '@' not in email or
            '.' not in email or
            email.index('@') > email.index('.')
        ):
            flash('Email must contain "@" before "."')
            return redirect(url_for('signup.signup'))

        # Validates password for strength
        # and allowed characters to improve security
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

        # Hashes the password before storing to protect user credentials
        hashed_pw = werkzeug.security.generate_password_hash(password)
        user_id = str(uuid.uuid4())
        db = get_db()
        cursor = db.cursor()
        # Checks for existing username or email to prevent duplicate accounts
        cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, email)
            )
        if cursor.fetchone():
            flash('Username or email already exists.')
            return redirect(url_for('signup.signup'))
        # Inserts the new user into the database after passing all checks
        cursor.execute(
            "INSERT INTO users (id, username, email, password) "
            "VALUES (?, ?, ?, ?)",
            (user_id, username, email, hashed_pw)
        )
        db.commit()
        db.close()
        flash('Sign up successful! Please log in.')
        return redirect(url_for('login.login'))
    # Renders the signup form for GET requests
    return render_template('pages/signup.html')
