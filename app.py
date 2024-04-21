from flask import Flask
from flask import render_template
from flask import request
from flask_bcrypt import Bcrypt 

import sqlite3
from flask import g

from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.filters import FILTERS

app = Flask(__name__)

DATABASE = 'db.db'

@app.template_filter('defaultQuantity')
def defaultQuantity(unit):
    if unit in ['ml', 'g']:
        return 100
    else:
        return 1

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/carts")
def create():
    return render_template('carts.html')


@app.route("/ingredients", methods=('GET', 'POST'))
def ingredients():

    message = ""
    show = ""

    if request.method == 'POST': 
        if not (
            request.form.get("name") 
            and request.form.get("unit") 
            and request.form.get("visibility")
            and (request.form.get("category") or request.form.get("categoryNew"))):
            message = "Please fill all of the neccessary fields!"

        else:
            rows = query_db('SELECT * FROM products WHERE name = ? COLLATE NOCASE', (request.form.get("name"),))

            if len(rows):
                message = f"{request.form.get('name').capitalize()} already exists in the list of products!"

            else:
                #TODO get author id - temporarily set as 1 (me)
                author = 1

                if request.form.get("category"):
                    category = request.form.get("category")
                else:
                    category = request.form.get("categoryNew")

                if request.form.get("visibility") == 'public':
                    visibility = 1
                else:
                    visibility = 0

                db = get_db()
                c = db.cursor()
                c.execute('INSERT INTO products(name, unit, category, author_id, date_added, public) VALUES (?, ?, ?, ?, datetime(), ?)',
                (request.form.get("name"), request.form.get("unit"), category, author, visibility))

                #query_db('INSERT INTO products(name, unit, category, author_id, date_added, public) VALUES (?, ?, ?, ?, datetime(), ?)',
                #(request.form.get("name"), request.form.get("unit"), category, author, visibility))
                db.commit()

                message = f"Added {request.form.get('name')} to the list of products!"

    #render products table
    products = query_db('SELECT product_id, name, category, unit FROM products GROUP BY name')
    categories = query_db('SELECT DISTINCT category FROM products')

    return render_template('ingredients.html', products=products, categories=categories, message=message)


@app.route("/recipes")
def recipes():
    return render_template('recipes.html')
