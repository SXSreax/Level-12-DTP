from flask import Flask, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()
# Create a table for heroes if it doesn't exist

app = Flask(__name__)

@app.route('/')   # Home page route(showing welcome message, some heros randomly selected from alll heros, and some heros from favorites if login, ai chator)
def home():
    return "Welcome to Marvel Rival Website!"

@app.route('/heroes')  #page showing all heros in the game, pictures, names, and basic details about them
def heroes():
    cursor.execute("SELECT image_url FROM Hero")
    heroes = cursor.fetchall()
    # Clean up the fetched data to extract the image URL
    image_urls = [row[0] for row in heroes]  # Assuming image_url is in the first column
    return render_template('Heroes.html', message=image_urls)# Assuming you have a heroes.html template

@app.route('/hero/<id>')  # Page showing details of a hero, including their powers, abilities, and backstory
def hero(id):
    # Fetch hero details
    cursor.execute("SELECT name, image_url, description FROM Hero WHERE id = ?", (id,))
    hero = cursor.fetchone()

    if not hero:
        return "Hero not found", 404

    hero_name = hero[0]
    hero_avatar = hero[1]
    hero_description = hero[2]

    # Fetch abilities
    cursor.execute("SELECT name, description FROM Abilities WHERE hero_id = ?", (id,))
    abilities = cursor.fetchall()  # List of (name, description)

    # Fetch skins
    cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id,))
    skins = cursor.fetchall()  # List of (skin_name, skin_image_url)

    return render_template(
        'hero.html',
        hero_name=hero_name,
        hero_avatar=hero_avatar,
        hero_description=hero_description,
        abilities=abilities,
        skins=skins
    )

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