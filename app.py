from flask import Flask, render_template
import sqlite3
from routes.home import home_bp
from routes.heroes import heroes_bp
from routes.hero import hero_bp
from routes.compare import compare_bp
from routes.login import login_bp
from routes.signup import sign_up_bp
from routes.favorite import favorite_bp
from routes.chat import chat_bp

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = '666'  # Add this line (use a strong, random value in production)

# routes for the website
app.register_blueprint(home_bp)

app.register_blueprint(heroes_bp)

app.register_blueprint(hero_bp)

app.register_blueprint(compare_bp)

app.register_blueprint(login_bp)

app.register_blueprint(sign_up_bp)

app.register_blueprint(favorite_bp)

app.register_blueprint(chat_bp)

if __name__ == '__main__': # Run the Flask app
    app.run(debug=True)
