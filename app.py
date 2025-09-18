from flask import Flask

from routes.pages.home import home_bp
from routes.pages.heroes import heroes_bp
from routes.pages.hero import hero_bp
from routes.pages.compare import compare_bp
from routes.pages.login import login_bp
from routes.pages.signup import sign_up_bp
from routes.pages.favorite import favorite_bp
from routes.components.chat import chat_bp
from routes.components.error_handlers import error_bp
from routes.pages.user import user_bp
from routes.components.context_processors import inject_profile_image

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'hahahahaha'

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(heroes_bp)
app.register_blueprint(hero_bp)
app.register_blueprint(compare_bp)
app.register_blueprint(login_bp)
app.register_blueprint(sign_up_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(error_bp)
app.register_blueprint(user_bp)

# Register context processor
app.context_processor(inject_profile_image)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
