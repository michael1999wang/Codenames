from flask import *
import sqlite3
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Red starts
    session['turn'] = "RED"

    # Read all words into a list
    lines = open('list.txt').read().splitlines()
    
    # Choose words for wordlist
    chosen = []
    for i in range (0, 25):
        randomChoice = random.choice(lines)
        chosen.append(randomChoice)
        lines.remove(randomChoice)

    session['wordList'] = chosen

    return render_template("index.html", team = session['turn'], word = session['wordList'])

@app.route('/game', methods=['GET', 'POST'])
def click():
    # Getting the word
    word = request.form["word"]

    # Instance of the database
    db = get_db()
    db.row_factory = make_dicts

    # Store the correct answer
    correct = query_db('select color from pairings where word = ?', [word], one=True)

    print(correct)

    # Close the database
    db.close()

    print(correct["color"] == session['turn'])

    # Swap teams if incorrect, otherwise keep going
    if correct["color"] != session['turn']:
        if session['turn'] == "RED":
            session['turn'] = "BLUE"
        else:
            session['turn'] = "RED"

    return render_template("index.html", team = session['turn'], word = session['wordList'])

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