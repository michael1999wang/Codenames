from flask import *
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", team = "RED")

@app.route('/')
def click():
    pass


DATABASE = './info.db'

#the function get_db is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3

def get_db():
    db=getattr(g,'_database', None)
    if db is None:
        db=g._database=sqlite3.connect(DATABASE)
    return db

#the function query_db is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    # rv return a list of dictionary
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


#the function make_dicts is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


#the function close_connection is taken from here
#https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.secret_key = '11111'
    app.run(debug=True) 