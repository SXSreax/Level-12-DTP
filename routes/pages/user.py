from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   session,
                   request,
                   flash)
import sqlite3
import werkzeug.security

user_bp = Blueprint('user', __name__)


def get_db():
    # Creates a database connection with row access by column name
    # for easier data handling
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    # Checks if the uploaded file has an allowed image extension
    # for security and consistency
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_bp.route('/user', methods=['GET', 'POST'])
def user_page():
    """
    Displays and updates the user's profile.

    Inputs:
        - Session data to identify the user.
        - POST form data for username, email, password, and profile image.

    Processing:
        - Redirects to login if user is not authenticated.
        - Handles profile image upload and validation.
        - Updates username and email if changed.
        - Changes password after verifying the old password.
        - Updates profile image in the database.
        - Provides feedback via flash messages.

    Outputs:
        - Renders the user.html template with updated profile info.
        - Redirects to login if user not found.
    """
    if 'user_id' not in session:
        # Prevents access to profile page for unauthenticated users
        return redirect(url_for('login.login'))

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        profile_pic = request.files.get('profile_pic')
        profile_image_url = None

        # Handles profile image upload and saves only allowed file types
        if profile_pic and allowed_file(profile_pic.filename):
            filename = werkzeug.utils.secure_filename(
                f"user_{session['user_id']}_{profile_pic.filename}"
                )
            filepath = f"static/images/{filename}"
            profile_pic.save(filepath)
            profile_image_url = f"images/{filename}"
        else:
            # Provides feedback if uploaded file is not an allowed image type
            if profile_pic and profile_pic.filename:
                flash(
                    "Only image files (png, jpg, jpeg, gif) are allowed.",
                    "error"
                    )

        # Updates username and email only if they have changed
        if username and email:
            cursor.execute(
                "SELECT username, email FROM users WHERE id=?",
                (session['user_id'],)
                )
            user = cursor.fetchone()
            if user and (username != user['username']
                         or email != user['email']):
                cursor.execute(
                    "UPDATE users SET username=?, email=? WHERE id=?",
                    (username, email, session['user_id'])
                )
                db.commit()
                flash("Username or email updated!", "success")

        # Handles password change after verifying the old password
        if old_password and new_password:
            cursor.execute(
                "SELECT password FROM users WHERE id=?",
                (session['user_id'],)
                )
            user = cursor.fetchone()
            if user and werkzeug.security.check_password_hash(user['password'],
                                                              old_password):
                hashed_pw = werkzeug.security.generate_password_hash(
                    new_password
                    )
                cursor.execute(
                    "UPDATE users SET password=? WHERE id=?",
                    (hashed_pw, session['user_id'])
                )
                db.commit()
                flash("Password changed successfully!", "success")
            else:
                # Notifies user if the current password is incorrect
                # or new password is invalid
                flash(
                    """Current password is incorrect
                    or new password is invalid!""",
                    "error")

        # Updates profile image in the database and provides feedback
        if profile_image_url:
            cursor.execute(
                "UPDATE users SET profile_image=? WHERE id=?",
                (profile_image_url, session['user_id'])
            )
            db.commit()
            flash("Profile image updated!", "success")

    # Retrieves the latest user info for display
    cursor.execute(
        "SELECT username, email, profile_image FROM users WHERE id = ?",
        (session['user_id'],)
        )
    user = cursor.fetchone()
    db.close()

    if not user:
        # Redirects to login if user record is missing
        return redirect(url_for('login.login'))

    # Uses default image if user has not set a profile image
    profile_image_url = (
        user['profile_image']
        if user['profile_image']
        else 'images/default.png'
    )

    # Renders the user profile page with current info
    return render_template(
        'pages/user.html',
        username=user['username'],
        email=user['email'],
        profile_image_url=profile_image_url
    )
