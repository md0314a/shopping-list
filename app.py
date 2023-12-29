from flask import Flask
from flask import render_template
from flask import request
from flask_bcrypt import Bcrypt 

import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = 'db.db'

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
    return render_template('create.html')


#SELECT MIN(id) AS id, title
#FROM tbl_countries
#GROUP BY title

@app.route("/ingredients", methods=('GET', 'POST'))
def ingredients():
    if request.method == 'GET': #browsing products
        products = query_db('SELECT product_id, name, unit FROM products GROUP BY name')
        return render_template('ingredients.html', products=products)

    return render_template('ingredients.html')

@app.route("/recipes")
def recipes():
    return render_template('recipes.html')
