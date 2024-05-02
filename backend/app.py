from flask import Flask
from flask import request
import functions
import sqlite3
from datetime import date

app = Flask(__name__)


@app.route('/courselookup') #/courselookup?course=nameofcourse&number=num
def lookup():
    course = request.args['course']
    number = request.args['number']
    sectiontoprof, profinfo = functions.func(f'{course} {number}')
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    params = (f'{course} {number}',)
    cur.execute("SELECT * FROM comments WHERE class = ?", params)
    print(cur.fetchall())
    comments = cur.fetchall()
    con.close()
    return [sectiontoprof, profinfo, comments]


@app.route('/prof', methods=['POST']) 
def rmp_comments():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    class_name = request.form["class_name"]
    return functions.fetchprof(f'{last_name} {first_name}', class_name)

@app.route('/coursecomments', methods=["POST"])
def postcomment(course, number):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    course = request.form["course"]
    number = request.form["number"]
    comment = request.form["comment"]
    data = (
    {"course": f'{course} {number}', "comment": comment ,"time": date.today()}
    )
    cur.execute("INSERT INTO comments VALUES(:course,:comment, :time)", data)
    con.commit()
    con.close()
    return "Ok"
