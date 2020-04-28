from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.secret_key = '11111'
    app.run(debug=True)