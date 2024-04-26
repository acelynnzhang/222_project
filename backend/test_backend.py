from app import app
import subprocess
from datetime import datetime, timedelta
import os, time, requests, base64, pytest, sys
import functions
import csv
from flask import request
import sqlite3
from datetime import date
import requests 

@pytest.fixture(autouse=True, scope='session')
def pytest_sessionstart():
    yield

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client

def check_course(test_client):
    # call the student's api and get the response
    r = test_client.get("/courselookup?course=CS&number=225")
    assert(r.status_code) == 200

    r = test_client.get("/courselookup?course=LOL&number=222")
    assert(r.status_code) == 400, f"invalid course did not return 400 response"

    r = test_client.get("/courselookup?course=AAS&number=215")
    assert(r.status_code) == 400, f"not offered course did not return 400 response"

    
def testdatabase(test_client):
    test_client.post('/coursecomments/CS/225', data={"comment": "testing database"}, content_type='multipart/form-data')
    r = test_client.get("/courselookup/CS/225")
    assert(r.status_code) == 200, f"whoops"

def testproffunc():
    should_work_prof= ["Solomon B", "Erickson J", "Sinha, M", "Hall S", "Curtis K"]
    class_names = ["CS 225", "CS 473", "CS 473", "ADV 150", ""]
    should_fail_prof = ["meow", "", "CS 225"]
    for i, prof in enumerate(should_work_prof):
        comments= functions.fetchprof(f'{prof}', class_names[i])
        assert(comments) != None, f'No commnet'
        print(comments)

    for prof in should_fail_prof:
        comments= functions.fetchprof(f'{prof}', "")
        assert(comments) != None, f'Should fail'


# with open('./data/gpa.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile, fieldnames=['Year','Term','YearTerm','Subject','Number','Course Title','Sched Type','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','W','Primary Instructor'])
#     for row in reader:
#         if row['Subject'] and row["Number"]:
#             print(row['Subject'], row["Number"])
#             #print(functions.func(row['Subject'] + ' ' + row["Number"]))
#             functions.func(row['Subject'] + ' ' + row["Number"])




# def postcomment(course, number):
#     con = sqlite3.connect("database.db")
#     cur = con.cursor()
#     #request.form["comment"]
#     data = (
#     {"course": f'{course} {number}', "comment": "help" ,"time": date.today()}
#     )
#     cur.execute("INSERT INTO comments VALUES(:course,:comment, :time)", data)
#     con.commit()
#     params = (f'{course} {number}',)
#     cur.execute("SELECT * FROM comments WHERE class = ?", params)
#     print(cur.fetchall())
#     con.close()

# def testapi(course, number):
#     #requests.get(f'http://127.0.0.1:5000/courselookup/{course}/{number}')
#     r = requests.post(f'http://127.0.0.1:5000/coursecomments/{course}/{number}', data= {"comment": "etwt"})
#     print(r.status_code)
#     con = sqlite3.connect("database.db")
#     cur = con.cursor()
#     params = (f'{course} {number}',)
#     cur.execute("SELECT * FROM comments WHERE class = ?", params)
#     print(cur.fetchall())
#     con.close()

# postcomment("CS", 255)
# testapi("CS", "255")
# con = sqlite3.connect("gpa.db")
# cur = con.cursor()
# params = ("CS 225","SOLOMON B",)
# print(cur.execute("SELECT avegpa,pastnumstudents FROM gpa WHERE class = ? AND prof = ?", params).fetchall())