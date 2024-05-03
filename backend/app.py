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
    sectiontoprof, profinfo = functions.class_info(f'{course} {number}')
    comments = functions.fetch_comments(course, number)
    if not sectiontoprof:
        return "Invalid course", 404
    if not profinfo:
        return "Other error in course API", 400
    return [sectiontoprof, profinfo, comments], 200


@app.route('/prof', methods=['POST']) 
def rmp_comments():
    print(request.form)
    rmp_summary = functions.fetch_prof(f'{request.json["last_name"]} {request.json["first_name"]}',f'{request.json["course"]} {request.json["number"]}')
    if not rmp_summary:
        return "Not in RateMyProfessor", 404
    return rmp_summary 

@app.route('/coursecomments', methods=["POST"])
def postcomment():
    functions.add_comment(f'{request.json["course"]}', f'{request.json["number"]}',f'{request.json["comment"]}')
    return "Ok"
