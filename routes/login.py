from flask import Blueprint, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')  #page for user login, including a form for entering username and password
def login():
    return render_template('login.html')