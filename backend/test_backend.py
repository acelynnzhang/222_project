from app import app
import pytest
import functions
import csv
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
    assert(r.status_code) == 404, f"invalid course did not return 404 response"

    r = test_client.get("/courselookup?course=AAS&number=215")
    assert(r.status_code) == 404, f"not offered course did not return 404 response"

class MockResponse:
    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}

def test_prof_func_api():
    should_work_prof= ["Solomon B", "Erickson J", "Hall S"]
    class_names = ["CS 225", "CS 473", "ADV 150"]
    
    for i, prof in enumerate(should_work_prof):
        comments= functions.fetch_prof(f'{prof}', class_names[i])
        assert(comments) != None, f'No comment on {prof} and {class_names[i]}'
        print(comments)


#curl -d '{"course":"CS", "number":"473","last_name": "Erickson", "first_name":"J"}' -H "Content-Type:  application/json" -X POST http://127.0.0.1:5000/prof"
def test_prof_func_cli(test_client):
    r = test_client.post('/prof', json={"course":"CS", "number":"473","last_name": "Erickson", "first_name":"J"})
    assert(r.status_code) == 200, f"courselookup error {r.text}"

    r = test_client.post('/prof', json={"course":"CS", "number":"225","last_name": "Solomon", "first_name":"B"})
    assert(r.status_code) == 200, f"courselookup error {r.text}"

    r = test_client.post('/prof', json={"course":"CS", "number":"225","last_name": "Beach", "first_name":"B"})
    assert(r.status_code) == 404, f"courselookup error {r.text}"

def test_func():
    num = 0
    with open('./data/gpa.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['Year','Term','YearTerm','Subject','Number','Course Title','Sched Type','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','W','Primary Instructor'])
        for row in reader:
            if num == 100:
                break
            if row['Subject'] and row["Number"]:
                print(row['Subject'], row["Number"])
                #print(functions.func(row['Subject'] + ' ' + row["Number"]))
                functions.class_info(row['Subject'] + ' ' + row["Number"])
            num += 1

def test_post_and_fetch_comment():
    class_names = ["CS 225", "CS 473", "CS 473", "ADV 150"]
    for x in class_names:
        x_split = x.upper().split()
        functions.add_comment(f'{x_split[0]}', f'{x_split[1]}', 'help')
        fetched = functions.fetch_comments(f'{x_split[0]}', f'{x_split[1]}')
        assert(('help', f'{date.today()}') in fetched), f'not in {fetched}'

def test_post_comment_cli(test_client):
    r= test_client.post('/coursecomments', json={"course":"MATH", "number":"241","comment": "testing database"})
    assert(r.status_code) == 200, f"whoops"

#curl -d '{"course":"CS", "number":"473","comment": "testing123testin123"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/coursecomments"
def test_post_fetch_comment_cli(test_client):
    class_names = ["CS 225", "CS 473", "CS 473", "ADV 150"]
    for x in class_names:
        x_split = x.upper().split()
        r = test_client.post('/coursecomments', json={"course":f'{x_split[0]}', "number":f'{x_split[1]}', "comment": "SOS"})
        assert(r.status_code) == 200, f'post commet failed'

        r = test_client.get(f"/courselookup?course={x_split[0]}&number={x_split[1]}")
        assert(['help', f'{date.today()}'] in r.json[2]), f"No msg found, {r.json[2]}"
