import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


# ---------------------------------------------------------------- search functionality
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


# ---------------------------------------------------------------- User registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        # if username does not already exist
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
            }
        mongo.db.users.insert_one(register)
        # put new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# ---------------------------------------------------------------- User login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # password does not match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username does not exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


# ---------------------------------------------------------------- User profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get session user's name from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    recipes = list(mongo.db.recipes.find(
        {"added_by": session["user"]}
    ))
    if session["user"]:
        return render_template(
            "profile.html", username=username, recipes=recipes)

    return redirect(url_for("login"))


# ---------------------------------------------------------------- User log out
@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# ---------------------------------------------------------------- User add recipe functionality
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":

        # check image url if one provided by user
        recipe_image = request.form.get("image_url")
        image_url = ""
        if recipe_image:
            # function call to verify image
            if is_url_image(recipe_image):
                image_url = recipe_image
                flash("Image verified")
            else:
                image_url = "../static/images/food.jpg"
                flash("Image not valid, will apply default image instead")

        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name").recipe(),
            "recipe_description": request.form.get("recipe_description"),
            "image_url": image_url,
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Your recipe has been successfully added")
        return redirect(url_for("profile", username=session["user"]))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipe.html", categories=categories)


# ---------------------------------------------------------------- User edit recipe functionality
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":

        # check image url if one provided by user
        recipe_image = request.form.get("image_url")
        image_url = ""
        if recipe_image:
            # function call to verify image
            if is_url_image(recipe_image):
                image_url = recipe_image
                flash("Image verified")
            else:
                image_url = "../static/images/new-zombie.jpg"
                flash("Image not valid, will apply default image instead")

        updated_recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name").recipe(),
            "recipe_description": request.form.get("recipe_description"),
            "image_url": image_url,
            }
        mongo.db.recipes.update_one(
            {"_id": ObjectId(recipe_id)}, {"$set": updated_recipe})
        flash("Your recipe has been successfully updated")
        return redirect(url_for("profile", username=session["user"]))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe, categories=categories)


# ---------------------------------------------------------------- User delete recipe functionality
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Your recipe has been deleted")
    return redirect(url_for("profile", username=session["user"]))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)