import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# initialize the app with the extension
db.init_app(app)

class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  added = db.Column(db.DateTime, default=datetime.datetime.now)

with app.app_context():
  db.create_all()


@app.route("/")
def root():
  recipes = db.session.execute(db.select(Recipe)).scalars()
  print(recipes)
  return render_template("index.html", recipes=recipes)

@app.route("/recipes/create", methods=["POST"])
def recipe_create():
  recipe = Recipe(name=request.form["name"])
  db.session.add(recipe)
  db.session.commit()
  return redirect(url_for("root"))