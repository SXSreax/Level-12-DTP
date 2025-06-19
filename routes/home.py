from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/') # Home page
def home(): 
    return render_template('home.html')