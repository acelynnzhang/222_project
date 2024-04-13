from flask import Flask
import functions


app = Flask(__name__)

profinfo = {}

@app.route('/courselookup/<course>/<number>')
def lookup(course, number):
    global profinfo
    profinfo = functions.func(f'{course} {number}')
    return profinfo


@app.route('/prof/<proffirst>/<proflast>')
def sum(proffirst,proflast):
    global profinfo
    if len(profinfo) < 1:
        raise Exception("no class given")
    prof = f'{proffirst}, {proflast}'
    if prof not in profinfo:
        raise Exception("prof not in info")
    return functions.fetchprof(profinfo[prof][0].ratemyprofid), 200