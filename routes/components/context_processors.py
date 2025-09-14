import sqlite3
from flask import session


def get_db():
    # Creates a database connection with row access by column name
    # for easier data handling
    conn = sqlite3.connect('databases/Heroes.db')
    conn.row_factory = sqlite3.Row
    return conn


def inject_profile_image():
    """
    Provides the user's profile image URL for use in all templates.

    Inputs:
        - Session data to identify the current user.

    Processing:
        - Uses a default image if the user is not logged in
            or has no profile image.
        - If the user is logged in, fetches their profile image.

    Outputs:
        - Returns a dictionary with 'profile_image_url' for template context.
    """
    # Default image for guests or users without a custom image
    profile_image_url = 'images/default.png'
    user_id = session.get('user_id')
    if user_id:
        db = get_db()
        cursor = db.cursor()
        # Retrieves the user's profile image
        # for personalized navigation and header
        cursor.execute("SELECT profile_image FROM users WHERE id = ?",
                       (user_id,))
        user = cursor.fetchone()
        db.close()
        if user and user['profile_image']:
            profile_image_url = user['profile_image']
    # Makes the profile image URL available to all templates via context
    return dict(profile_image_url=profile_image_url)
