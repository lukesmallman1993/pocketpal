import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_paginate import Pagination, get_page_args
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

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 4
    offset = (page - 1) * per_page
    total = mongo.db.recipes.find().count()
    recipes = mongo.db.recipes.find()
    recipes_paginated = recipes[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total, css_framework='materializecss')
    return render_template("index.html", recipes=recipes_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
                           
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
   
    if request.method == "POST":
        recipe = {
            "meal_name": request.form.get("pizza_name"),
            "meal_description": request.form.get("short_description"),
            "category_name": request.form.getlist("category_name"),
            "ingredients": request.form.getlist("ingredients"),
            "cooking_steps": request.form.getlist("cooking_steps"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Thank you for submitting your recipe!")
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipe.html", categories=categories)


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
   
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view_recipe.html", recipe=recipe)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)