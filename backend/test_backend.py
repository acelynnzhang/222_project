from app import app
import subprocess
from datetime import datetime, timedelta
import os, time, requests, base64, pytest, sys
import functions
import csv
from flask import request
import sqlite3
from datetime import date

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

def test_check_course(test_client):
    # call the student's api and get the response
    r = test_client.get("/courselookup?course=CS&number=225")
    assert(r.status_code) == 200

    r = test_client.get("/courselookup?course=LOL&number=222")
    assert(r.status_code) == 400, f"invalid course did not return 400 response"

    r = test_client.get("/courselookup?course=AAS&number=215")
    assert(r.status_code) == 400, f"not offered course did not return 400 response"

    
def test_testdatabase(test_client):
    test_client.post('/coursecomments', json={"course":"CS", "number":"225","comment": "testing database"})
    r = test_client.get("/courselookup?course=CS&number=225")
    assert(r.status_code) == 200, f"whoops"

def test_prof_func():
    should_work_prof= ["Solomon B", "Erickson J", "Hall S"]
    class_names = ["CS 225", "CS 473", "ADV 150"]
    
    for i, prof in enumerate(should_work_prof):
        comments= functions.fetch_prof(f'{prof}', class_names[i])
        assert(comments) != None, f'No comment on {prof} and {class_names[i]}'
        print(comments)

    #should_fail_prof = ["meow", "", "CS 225"]
    # for prof in should_fail_prof:
    #     comments= functions.fetchprof(f'{prof}', "")
    #     assert(comments) == [], f'Should fail'
    #never returns I dunno why

#curl -d '{"course":"CS", "number":"473","last_name": "Erickson", "first_name":"J"}' -H "Content-Type:  application/json" -X POST http://127.0.0.1:5000/prof"
def test_prof_func_cli(test_client):
    r = test_client.post('/prof', data={"course":"CS", "number":"473","last_name": "Erickson", "first_name":"J"}, content_type='application/json')
    assert(r.status_code) == 200, f"whoops"

    r = test_client.post('/prof', data={"course":"CS", "number":"225","last_name": "Solomon", "first_name":"B"}, content_type='application/json')
    assert(r.status_code) == 200, f"whoops"

# def test_func():
#     with open('./data/gpa.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile, fieldnames=['Year','Term','YearTerm','Subject','Number','Course Title','Sched Type','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','W','Primary Instructor'])
#         for row in reader:
#             if row['Subject'] and row["Number"]:
#                 print(row['Subject'], row["Number"])
#                 #print(functions.func(row['Subject'] + ' ' + row["Number"]))
#                 functions.class_info(row['Subject'] + ' ' + row["Number"])




def test_post_and_fetch_comment():
    class_names = ["CS 225", "CS 473", "CS 473", "ADV 150"]
    for x in class_names:
        x_split = x.upper().split()
        functions.add_comment(f'{x_split[0]}', f'{x_split[1]}', 'help')
        fetched = functions.fetch_comments(f'{x_split[0]}', f'{x_split[1]}')
        assert(('help', f'{date.today()}') in fetched), f'not in {fetched}'


#curl -d '{"course":"CS", "number":"473","comment": "testing123testin123"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/coursecomments"
def test_post_comment_cli(test_client):
    class_names = ["CS 225", "CS 473", "CS 473", "ADV 150"]
    for x in class_names:
        x_split = x.upper().split()
        r = test_client.post('/coursecomments', data={"course":f'{x_split[0]}', "number":f'{x_split[1]}', "comment": "SOS"}, content_type='application/json')
        assert(r.status_code) == 200, f'post commet failed'

        r = test_client.get(f"/courselookup?course={x_split[0]}&number={x_split[1]}")
        assert(('help', f'{date.today()}') in r[2]), "No msg found"

# postcomment("CS", 255)
# testapi("CS", "255")
# con = sqlite3.connect("gpa.db")
# cur = con.cursor()
# params = ("CS 225","SOLOMON B",)
# print(cur.execute("SELECT avegpa,pastnumstudents FROM gpa WHERE class = ? AND prof = ?", params).fetchall())