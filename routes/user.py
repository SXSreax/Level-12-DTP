from flask import Blueprint, render_template, redirect, url_for, session, request, flash
import sqlite3
import werkzeug.security

user_bp = Blueprint('user', __name__)

def get_db():
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/user', methods=['GET', 'POST'])
def user_page():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        updated = False

        username = request.form.get('username')
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        profile_pic = request.files.get('profile_pic')
        profile_image_url = None

        # Handle profile image upload
        if profile_pic and allowed_file(profile_pic.filename):
            filename = werkzeug.utils.secure_filename(f"user_{session['user_id']}_{profile_pic.filename}")
            filepath = f"static/images/{filename}"
            profile_pic.save(filepath)
            profile_image_url = f"images/{filename}"
        else:
            if profile_pic and profile_pic.filename:
                flash("Only image files (png, jpg, jpeg, gif) are allowed.", "error")

        # Username/email/profile image update
        if username and email:
            # Only update if changed
            cursor.execute("SELECT username, email FROM users WHERE id=?", (session['user_id'],))
            user = cursor.fetchone()
            if user and (username != user['username'] or email != user['email']):
                cursor.execute(
                    "UPDATE users SET username=?, email=? WHERE id=?",
                    (username, email, session['user_id'])
                )
                db.commit()
                flash("Username or email updated!", "success")
                updated = True

        # Password change logic
        if old_password and new_password:
            cursor.execute("SELECT password FROM users WHERE id=?", (session['user_id'],))
            user = cursor.fetchone()
            if user and werkzeug.security.check_password_hash(user['password'], old_password):
                hashed_pw = werkzeug.security.generate_password_hash(new_password)
                cursor.execute(
                    "UPDATE users SET password=? WHERE id=?",
                    (hashed_pw, session['user_id'])
                )
                db.commit()
                flash("Password changed successfully!", "success")
                updated = True
            else:
                flash("Current password is incorrect or new password is invalid!", "error")

        # Profile image update (if you want feedback)
        if profile_image_url:
            cursor.execute(
                "UPDATE users SET profile_image=? WHERE id=?",
                (profile_image_url, session['user_id'])
            )
            db.commit()
            flash("Profile image updated!", "success")
            updated = True

    cursor.execute("SELECT username, email, profile_image FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    db.close()

    if not user:
        return redirect(url_for('login.login'))

    profile_image_url = user['profile_image'] if user['profile_image'] else 'images/default.png'

    return render_template(
        'user.html',
        username=user['username'],
        email=user['email'],
        profile_image_url=profile_image_url
    )