from flask import Flask

app = Flask(__name__)

@app.route('/')   # Home page route(showing welcome message, some heros randomly selected from alll heros, and some heros from favorites if login, ai chator)
def home():
    return "Welcome to Marvel Rival Website! test"''

@app.route('/heroes')  #page showing all heros in the game, pictures, names, and basic details about them
def heroes():
    return "List of Marvel Heroes"

@app.route('/hero/<id>')  #page showing details of a hero, including their powers, abilities, and backstory
def hero(id):
    return f"Details of Hero with ID: {id}"

@app.route('/compare/<id1>/<id2>')  #page allowing users to compare two heroes side by side, showing their stats and abilities
def compare(id1, id2):
    return f"Comparing Hero {id1} with Hero {id2}"

@app.route('/login')  #page for user login, including a form for entering username and password
def login():
    return "Login Page"

@app.route('/signup')  #page for user signup, including a form for entering username, password, and email
def signup():
    return "Signup Page"

@app.route('/favorites')  #page showing user's favorite heroes, allowing them to add or remove heroes from their favorites list
def favorites():
    return "List of Favorite Heroes"

if __name__ == '__main__':
    app.run(debug=True)