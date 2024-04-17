from flask import Flask
from flask import request
import functions
import sqlite3
from datetime import date

app = Flask(__name__)

profinfo = {}
sectiontoprof = {}

@app.route('/courselookup/<course>/<number>')
def lookup(course, number):
    global profinfo
    sectiontoprof, profinfo = functions.func(f'{course} {number}')
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    params = (f'{course} {number}',)
    cur.execute("SELECT * FROM comments WHERE class = ?", params)
    print(cur.fetchall())
    comments = cur.fetchall()
    con.close()
    return [sectiontoprof, profinfo, comments]


@app.route('/prof/<proffirst>/<proflast>')
def sum(proffirst,proflast):
    global profinfo
    if len(profinfo) < 1:
        raise Exception("no class given")
    prof = f'{proffirst}, {proflast}'
    if prof not in profinfo:
        raise Exception("prof not in info")
    return functions.fetchprof(profinfo[prof][0])

@app.route('/coursecomments/<course>/<number>', methods=["POST"])
def postcomment(course, number):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    comment = request.form["comment"]
    data = (
    {"course": f'{course} {number}', "comment": comment ,"time": date.today()}
    )
    cur.execute("INSERT INTO comments VALUES(:course,:comment, :time)", data)
    con.commit()
    con.close()
    return "Ok"
