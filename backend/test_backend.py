from app import app
import subprocess
from datetime import datetime, timedelta
import os, time, requests, base64, pytest, sys

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
    r = test_client.get("/courselookup/CS/225")
    assert(r.status_code) == 200

    r = test_client.get("/courselookup/LOL/222")
    assert(r.status_code) == 400, f"invalid course did not return 400 response"

    r = test_client.get("/courselookup/AAS/215")
    assert(r.status_code) == 400, f"not offered course did not return 400 response"

    
def testdatabase(test_client):
    test_client.post('/coursecomments/CS/225', data={"comment": "testing database"}, content_type='multipart/form-data')
    r = test_client.get("/courselookup/CS/225")
    assert(r.status_code) == 200, f"whoops"



