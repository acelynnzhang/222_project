from flask import Flask
import testing

app = Flask(__name__)

@app.route('/courselookup/<course>/<number>')
def lookup(course, number):
    testing.func(f'{course} {number}')
