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

chomiryo_list = [
  {"key": "sato", "display": "砂糖"},
  {"key": "shio", "display": "塩"},
  {"key": "shoyu", "display": "醤油"},
  {"key": "mirin", "display": "みりん"},
  {"key": "sake", "display": "さけ"},
  {"key": "su", "display": "酢"},
]

class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String, nullable=False)
  image_path = db.Column(db.String)
  memo = db.Column(db.String)
  created_date = db.Column(db.DateTime, default=datetime.datetime.now)

# Chomiryo
for chomiryo in chomiryo_list:
  setattr(Recipe, chomiryo["key"], db.Column(db.Integer, default=0))

# Database creatione if needed
with app.app_context():
  db.create_all()

# Routing

@app.route("/")
def root():
  recipes = db.session.execute(db.select(Recipe)).scalars()
  return render_template("index.html", recipes=recipes, chomiryo_list=chomiryo_list)

@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def recipe(recipe_id):
  record = db.select(Recipe).filter_by(id=recipe_id)
  recipe = db.session.execute(record).scalar_one()
  return render_template("recipes/recipe.html", recipe=recipe, chomiryo_list=chomiryo_list)

@app.route("/recipes/create", methods=["GET", "POST"])
def recipe_create():
  if request.method == "POST":
    chomiryo_dict = {}
    for chomiryo in chomiryo_list:
      key = chomiryo["key"]
      chomiryo_dict[key] = request.form[key]

    recipe = Recipe(
      name=request.form["name"],
      memo=request.form["memo"],
      **chomiryo_dict,
    )
    db.session.add(recipe)
    db.session.commit()
    return redirect(url_for("root"))
  
  return render_template('recipes/create.html', chomiryo_list=chomiryo_list)

@app.route("/recipes/delete", methods=["POST"])
def recipe_delete():
  id = request.form["id"]
  record = db.select(Recipe).filter_by(id=id)
  recipe = db.session.execute(record).scalar_one()
  db.session.delete(recipe)
  db.session.commit()
  return redirect(url_for("root"))