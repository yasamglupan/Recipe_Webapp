from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask (__name__)

@app.route('/')
def home():
    return render_template("home.html", title = "Home")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Here you can process the contact form data, such as sending an email
        return "Thank you for your message, " + name + "!"

    return render_template('contact.html')


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
    cur.execute("SELECT * FROM Recipe_Ingredients WHERE recipe_id=?", (recipe[0],))
    quantity = cur.fetchall()
    cur.execute('SELECT * FROM Review WHERE recipe_id=?',(id,))
    reviews = cur.fetchall()
    
    return render_template('recipe.html', recipe = recipe, ingredients = ingredients,reviews = reviews,quantity=quantity)


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
