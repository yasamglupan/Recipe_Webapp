from flask import Flask, render_template, redirect, request, url_for, abort
import sqlite3

app = Flask(__name__)


def retrive_query_results(sql_statement, fetch_method="all", values=None):
    """
    This is a function that takes a sql statment, opens a connection, runs the sql query, and
    either commits or fetches the results and returns the results

    :sql_statment: This is the sql query
    :fetch_method: This confuirms if to fetch one, fetch all, or fetch no results
    :values: If values are passed exicute with the values
    :return: returns the results of the query sql_statment
    """
    conn = sqlite3.connect('recipe.db')
    cur = conn.cursor()
    if values:  # if values are passed exicute with the values
        cur.execute(sql_statement, values)  # Pass values as a tuple
    else:
        cur.execute(sql_statement)
    if fetch_method == "one":  # Fetch one
        result = cur.fetchone()
    elif fetch_method == "none":  # Commit
        conn.commit()
        result = None  # Return None when no fetch is needed
    else:  # Fetch all
        result = cur.fetchall()
    conn.close()
    return result


# Route for home page
@app.route('/')
def home():
    return render_template("home.html", title="Home")


# Route for contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Process the contact form data, such as sending an email
        # In a real application, you would typically handle the form data here
        sql_statement = "INSERT INTO Contact (name, email, message)\
                        VALUES (?, ?, ?)"
        retrive_query_results(sql_statement, "none", (name, email, message))
    return render_template('contact.html')


# Route for about page
@app.route('/about')
def about():
    return render_template("about.html", title="About")


# Route for All recipes page
@app.route('/all_recipes')
def all_recipes():
    # Execute an SQL query to retrieve all records from the Recipe table
    sql_statement = "SELECT * FROM Recipe"
    # Fetch all records through the retrive_query_results function
    results = retrive_query_results(sql_statement)
    return render_template('all_recipes.html', results=results)


# Route for individual recipes page
@app.route('/recipe/<int:id>')
def recipe(id):
    sql_statement = "SELECT * FROM Recipe WHERE recipe_id={}".format(id)
    # Execute an SQL query to retrieve a specific recipe by ID
    recipe = retrive_query_results(sql_statement, "one")
    if recipe is None:
        abort(404)  # Raise a 404 error if the recipe doesn't exist
    # Execute an SQL query to retrieve ingredient names for the recipe
    sql_statement = "SELECT Ingredients.name, Recipe_Ingredients.quantity\
                    FROM Ingredients \
                    JOIN Recipe_Ingredients ON Ingredients.id = Recipe_Ingredients.ingredient_id\
                    WHERE Recipe_Ingredients.recipe_id = {}".format(id)
    ingredients = retrive_query_results(sql_statement)
    # Execute an SQL query to retrieve reviews for the recipe
    sql_statement = "SELECT * FROM Review WHERE recipe_id={}".format(id)
    reviews = retrive_query_results(sql_statement)
    return render_template('recipe.html',
                            recipe=recipe,
                            ingredients=ingredients,
                            reviews=reviews)


# Route for adding reviews
@app.route('/recipes', methods=['POST'])
def add_recipes():
    name = request.form['name']
    review = request.form['review']
    rating = request.form['rating']
    recipe_id = request.form['recipe_id']
    # Execute an SQL query to insert a new review into the Review table
    sql_statement = "INSERT INTO Review (name, rating, review, recipe_id)\
                    VALUES (?, ?, ?, ?)"
    retrive_query_results(sql_statement, "none", (name, rating, review, recipe_id))
    return redirect(url_for("recipe", id=recipe_id))


# Route for the 404 error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
