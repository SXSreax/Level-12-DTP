from flask import Blueprint, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()

sign_up_bp = Blueprint('signup', __name__)

@sign_up_bp.route('/signup')  #page for user signup, including a form for entering username, password, and email
def signup():
    return render_template('sign_up.html') 