from flask import Flask, render_template, redirect, request, url_for
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
    cur.execute('SELECT name FROM Ingredients WHERE id IN(SELECT ingredient_id FROM Recipe_Ingredients WHERE recipe_id=?)',(id,))
    ingredients = cur.fetchall()
    cur.execute('SELECT quantity, unit FROM Recipe_Ingredients WHERE recipe_id=?',(id,))
    cur.execute('SELECT * FROM Review WHERE recipe_id=?',(id,))
    reviews = cur.fetchall()
    
    return render_template('recipe.html', recipe = recipe, ingredients = ingredients,reviews = reviews)


@app.route('/recipes', methods=['POST']) 
def add_recipes(): 
    conn = sqlite3.connect('recipe.db') 
    name = request.form['name'] 
    review = request.form['review'] 
    rating = request.form['rating']
    recipe_id = request.form['recipe_id'] 
    conn = sqlite3.connect('recipe.db') 
    cursor = conn.cursor() 
    cursor.execute('INSERT INTO Review (name, rating, review, recipe_id) VALUES (?, ?, ?, ?)', (name, rating, review, recipe_id)) 
    conn.commit() 
    return redirect(url_for("recipe", id=recipe_id))

if __name__ == "__main__":
    app.run(debug=True)

