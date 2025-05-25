from flask import Flask, render_template
import sqlite3

conn = sqlite3.connect('databases/Heroes.db', check_same_thread=False)
cursor = conn.cursor()
# Create a table for heroes if it doesn't exist

app = Flask(__name__)

@app.route('/')   # Home page route(showing welcome message, some heros randomly selected from alll heros, and some heros from favorites if login, ai chator)
def home():
    return render_template('home.html')

@app.route('/heroes')  #page showing all heros in the game, pictures, names, and basic details about them
def heroes():
    cursor.execute("SELECT id, image_url FROM Hero")
    heroes = cursor.fetchall()  # List of (id, image_url)
    return render_template('heroes.html', heroes=heroes)

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
    cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id,))
    abilities = cursor.fetchall()  # List of (name, description)

    # Fetch skins
    cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id,))
    skins = cursor.fetchall()  # List of (skin_name, skin_image_url)

    print(hero_avatar)

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
    # Fetch hero 1 details
    cursor.execute("SELECT name, image_url, description FROM Hero WHERE id = ?", (id1,))
    h1 = cursor.fetchone()
    cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id1,))
    h1_abilities = cursor.fetchall()
    cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id1,))
    h1_skins = cursor.fetchall()

    # Fetch hero 2 details
    cursor.execute("SELECT name, image_url, description FROM Hero WHERE id = ?", (id2,))
    h2 = cursor.fetchone()
    cursor.execute("SELECT ability_name, description FROM Abilities WHERE hero_id = ?", (id2,))
    h2_abilities = cursor.fetchall()
    cursor.execute("SELECT skin_name, skin_image_url FROM Skins WHERE hero_id = ?", (id2,))
    h2_skins = cursor.fetchall()

    hero1 = {
        "name": h1[0], "image_url": h1[1], "description": h1[2],
        "abilities": h1_abilities, "skins": h1_skins
    }
    hero2 = {
        "name": h2[0], "image_url": h2[1], "description": h2[2],
        "abilities": h2_abilities, "skins": h2_skins
    }
    return render_template('compare.html', hero1=hero1, hero2=hero2)

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