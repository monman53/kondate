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
  image_path = db.Column(db.String)
  memo = db.Column(db.String)
  created_date = db.Column(db.DateTime, default=datetime.datetime.now)

  # Chomiryo
  shoyu = db.Column(db.Integer, default=0)
  sato = db.Column(db.Integer, default=0)
  mirin = db.Column(db.Integer, default=0)
  shio = db.Column(db.Integer, default=0)
  su = db.Column(db.Integer, default=0)
  sake = db.Column(db.Integer, default=0)

with app.app_context():
  db.create_all()


@app.route("/")
def root():
  recipes = db.session.execute(db.select(Recipe)).scalars()
  return render_template("index.html", recipes=recipes)

@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def recipe(recipe_id):
  record = db.select(Recipe).filter_by(id=recipe_id)
  recipe = db.session.execute(record).scalar_one()
  return render_template("recipes/recipe.html", recipe=recipe)

@app.route("/recipes/create", methods=["GET", "POST"])
def recipe_create():
  if request.method == "POST":
    recipe = Recipe(
      name=request.form["name"],
      memo=request.form["memo"],
      
      # Chomiryo
      shoyu=request.form["shoyu"],
      sato=request.form["sato"],
      mirin=request.form["mirin"],
      shio=request.form["shio"],
      su=request.form["su"],
      sake=request.form["sake"],
    )
    db.session.add(recipe)
    db.session.commit()
    return redirect(url_for("root"))
  
  return render_template('recipes/create.html')

@app.route("/recipes/delete", methods=["POST"])
def recipe_delete():
  id = request.form["id"]
  record = db.select(Recipe).filter_by(id=id)
  recipe = db.session.execute(record).scalar_one()
  db.session.delete(recipe)
  db.session.commit()
  return redirect(url_for("root"))