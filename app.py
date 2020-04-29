from flask import *
import sqlite3
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    session['turn'] = "RED" # Red starts
    session['wordList'] = generateWordList() # Store wordlist in session data
    session['colorList'] = generateColorList() # Store colorList in session data
    session['classList'] = generateClassList() # Store the classList in session data
    matchPairings() # Updates the SQL

    return render_template("index.html", team = session['turn'], word = session['wordList'], classes = session['classList'])


@app.route('/game', methods=['GET', 'POST'])
def click():
    # Getting the word
    word = request.form["word"]

    # Instance of the database
    db = get_db()
    db.row_factory = make_dicts

    # Store the correct answer
    correct = query_db('select color from pairings where word = ?', [word], one=True)

    # Close the database
    db.close()

    # Assigning the color after choice
    session['classList'][session['wordList'].index(word)] = correct["color"]

    # Swap teams if incorrect, otherwise keep going
    if correct["color"] != session['turn']:
        if session['turn'] == "RED":
            session['turn'] = "BLUE"
        else:
            session['turn'] = "RED"

    return render_template("index.html", team = session['turn'], word = session['wordList'], classes = session['classList'])


def generateWordList():
    # Read all words into a list
    lines = open('list.txt').read().splitlines()
    
    # Choose words for wordlist
    chosen = []
    for i in range (0, 25):
        randomChoice = random.choice(lines)
        chosen.append(randomChoice)
        lines.remove(randomChoice)

    # Returns wordlist
    return chosen


def generateColorList():
    colors = []
    redCount, blueCount, neutralCount = 0, 0, 0

    # Keep generating colors 8 of each color and 9 neutrals
    while (redCount + blueCount + neutralCount < 25):
        rng = random.randint(0, 100)
        if rng < 33 and redCount < 8:
            colors.append("RED")
            redCount += 1
        elif rng < 66 and blueCount < 8:
            colors.append("BLUE")
            blueCount += 1
        else:
            if neutralCount < 9:
                colors.append("NEUTRAL")
                neutralCount += 1
    
    # Pick one neutral to turn into the lose card
    deep = random.randint(0,9)
    for i in range(0, 25):
        if colors[i] == "NEUTRAL":
            if deep == 0:
                colors[i] = "LOSS"
                break
            deep -= 1

    # Returns colorList
    return colors


def generateClassList():
    classes = []
    for i in range (0, 25):
        classes.append("DEFAULT")
    return classes


def matchPairings():
    # Instance of the database
    db = get_db()
    db.row_factory = make_dicts
    cur = db.cursor()

    # Drop the existing table
    cur.execute('drop table if exists pairings')

    # Create new table
    cur.execute('create table pairings (word VARCHAR(255), color VARCHAR(255))')

    # Add all pairings into the database
    for i in range (0, 24):
        cur.execute('insert into pairings (word, color) values (?, ?)', [session['wordList'][i], session['colorList'][i]])

    # Commit and close the database
    db.commit()
    cur.close()
    db.close()


# ---------------------------- DATABASE FUNCTIONS ----------------------------
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