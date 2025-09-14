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


def get_db():
    # Creates a database connection with row access by column name
    # for easier data handling
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    Inputs:
        - POST request with 'username' and 'password' from the login form.

    Processing:
        - Checks credentials against the database.
        - Verifies password using secure hash comparison.
        - Sets session variables if login is successful.
        - Provides feedback via flash messages.

    Outputs:
        - Redirects to home page on success.
        - Redirects back to login page with error message on failure.
        - Renders login page for GET requests.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        # Looks up the user by username to validate credentials
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        db.close()
        if user and werkzeug.security.check_password_hash(
            user['password'], password
        ):
            # Stores user info in session for authentication across pages
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!')
            return redirect(url_for('home.home'))
        else:
            # Notifies user of failed login attempt for clarity
            flash('Invalid username or password.')
            return redirect(url_for('login.login'))
    # Shows the login form for GET requests
    return render_template('pages/login.html')


@login_bp.route('/logout')
def logout():
    """
    Logs the user out by clearing session data.

    Inputs:
        None.

    Processing:
        - Clears all session variables to remove authentication.
        - Notifies user of logout.

    Outputs:
        Redirects to login page with a flash message.
    """
    session.clear()  # Removes all user data from session for security
    flash('You have been logged out.')
    return redirect(url_for('login.login'))
