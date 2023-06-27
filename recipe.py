from flask import Flask, render_template
import sqlite3


app = Flask (__name__)

@app.route('/')
def home():
    return render_template("home.html", title = "Home")

@app.route('/contact')
def contact():
    return render_template("contact.html", title = "Contact")

@app.route('/about')
def about():
    return render_template("about.html", title = "About")

@app.route('/all_recipes')
def all_recipes():
    conn = sqlite3.connect('recipe.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Recipe')
    results = cur.fetchall()
    return render_template('all_recipes.html', results = results)

@app.route('/recipe/<int:id>')
def recipe(id):
    conn = sqlite3.connect('recipe.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Recipe WHERE recipe_id=?',(id,))
    recipe = cur.fetchone()
    print (recipe)
    # cur.execute('SELECT name FROM Recipe_Ingredients WHERE id=?',(recipe[4],))
    # base = cur.fetchone()
    # cur.execute('SELECT name FROM Toppings WHERE id IN(SELECT tid FROM PizzaToppings WHERE pid=?)',(id,))
    # toppings = cur.fetchall()
    
    return render_template('recipe.html', recipe = recipe)

if __name__ == "__main__":
    app.run(debug=True)
