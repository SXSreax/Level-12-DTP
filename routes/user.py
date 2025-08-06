from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET', 'POST'])
def signup():

    return render_template('user.html')