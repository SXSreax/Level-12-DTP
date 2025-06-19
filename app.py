from flask import Flask, render_template
import sqlite3
from routes.home import home_bp
from routes.heroes import heroes_bp
from routes.hero import hero_bp
from routes.compare import compare_bp
from routes.login import login_bp
from routes.sign_up import sign_up_bp
from routes.favorite import favorite_bp


conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()
# Create a table for heroes if it doesn't exist

app = Flask(__name__)

app.register_blueprint(home_bp)

app.register_blueprint(heroes_bp)

app.register_blueprint(hero_bp)

app.register_blueprint(compare_bp)

app.register_blueprint(login_bp)

app.register_blueprint(sign_up_bp)

app.register_blueprint(favorite_bp)

if __name__ == '__main__': # Run the Flask app
    app.run(debug=True)
