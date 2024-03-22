import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
import csv

@dataclass
class Classsection:
    section: str
    CRN: int
    instructor: str
    enrollmentstatus: str
    starttime: str
    endtime: str
    days: str
    meetingplace: str
    ratemyprofid: str
    ratemyprof: list
    pastnumstudents: int
    pastavegpa: int


YEAR = 2024
SEM = "fall"


gpadict = {}
#dictionary of teachers that maps to dictionary of their classes and ave gpa + num students

with open('./data/gpa.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['Year','Term','YearTerm','Subject','Number','Course Title','Sched Type','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','W','Primary Instructor'])
    for row in reader:
        if row['Primary Instructor']:
            name = row['Primary Instructor'].split(', ')
            name = name[0].strip(',').upper() + ' ' + name[1][0].upper()
            if name not in gpadict:
                gpadict[name] ={}
            totnum = int(row['A+'])+ int(row['A'])+int(row['A-'])+int(row['B+'])+ int(row['B'])+int(row['B-'])+int(row['C+'])+ int(row['C'])+int(row['C-'])+int(row['D+'])+ int(row['D'])+int(row['D-'])+int(row['F'])
            sumpoints = (int(row['A+']) + int(row['A']))* 4.0 +int(row['A-'])* 3.67+int(row['B+'])*3.33+ int(row['B'])*3+int(row['B-'])*2.67+int(row['C+'])* 2.33+ int(row['C'])*2+int(row['C-']) * 1.67+int(row['D+']) * 1.33+ int(row['D']) *1+int(row['D-'])*0.67 
            classnum = row['Subject'] + ' ' + row['Number']
            if classnum  in gpadict[name]:
                gpadict[name][classnum ]['sumtot'] += sumpoints
                gpadict[name][classnum ]['sumstudents'] += totnum
            else:
                gpadict[name][classnum ] = {'sumtot':sumpoints, 'sumstudents':totnum}

def givestats(instructor,classname):
    a = 0
    b = 0
    print(classname)
    if instructor in gpadict and classname in gpadict[instructor]:
        b = gpadict[instructor][classname]['sumstudents']
        a = gpadict[instructor][classname]['sumtot']/b
    print((a,b))
    return (a,b)
#retrive basic info from ratemyprof
def basicinfo(lastname, firstletter):

    headers = {"Authorization": "Basic dGVzdDp0ZXN0"}

    json_data = {
        "query": "query NewSearchTeachersQuery(\n  $query: TeacherSearchQuery!\n  $count: Int\n) {\n  newSearch {\n    teachers(query: $query, first: $count) {\n      didFallback\n      edges {\n        cursor\n        node {\n          id\n          legacyId\n          firstName\n          lastName\n          department\n          departmentId\n          school {\n            legacyId\n            name\n            id\n          }\n          ...CompareProfessorsColumn_teacher\n        }\n      }\n    }\n  }\n}\n\nfragment CompareProfessorsColumn_teacher on Teacher {\n  id\n  legacyId\n  firstName\n  lastName\n  school {\n    legacyId\n    name\n    id\n  }\n  department\n  departmentId\n  avgRating\n  numRatings\n  wouldTakeAgainPercentRounded\n  mandatoryAttendance {\n    yes\n    no\n    neither\n    total\n  }\n  takenForCredit {\n    yes\n    no\n    neither\n    total\n  }\n  ...NoRatingsArea_teacher\n  ...RatingDistributionWrapper_teacher\n}\n\nfragment NoRatingsArea_teacher on Teacher {\n  lastName\n  ...RateTeacherLink_teacher\n}\n\nfragment RatingDistributionWrapper_teacher on Teacher {\n  ...NoRatingsArea_teacher\n  ratingsDistribution {\n    total\n    ...RatingDistributionChart_ratingsDistribution\n  }\n}\n\nfragment RatingDistributionChart_ratingsDistribution on ratingsDistribution {\n  r1\n  r2\n  r3\n  r4\n  r5\n}\n\nfragment RateTeacherLink_teacher on Teacher {\n  legacyId\n  numRatings\n  lockStatus\n}\n",
        "variables": {
            "query": {
                "text": lastname + " " + firstletter,
                "schoolID": "U2Nob29sLTExMTI=",
            },
            "count": 10,
        },
    }

    response = requests.post(
        "https://www.ratemyprofessors.com/graphql", headers=headers, json=json_data
    )
    # print(response.text)
    r = response.json()
    for thing in r["data"]["newSearch"]["teachers"]["edges"]:
        if (
            thing["node"]["lastName"].upper() == lastname
            and thing["node"]["firstName"][0].upper() == firstletter
        ):
            big = "tot"
            currval = 0
            for key in thing["node"]["mandatoryAttendance"]:
                if (
                    key != "total"
                    and thing["node"]["mandatoryAttendance"][key] > currval
                ):
                    big = key
            return (
                thing["node"]["id"],
                [
                    thing["node"]["avgRating"],
                    big,
                    thing["node"]["ratingsDistribution"]["total"],
                    thing["node"]["wouldTakeAgainPercentRounded"],
                ],
            )

    return "None"


def func(boop):
    classnam = boop.upper()
    classnam = classnam.split()  # need courses in CS 222 format
    r = requests.get(
        f"http://courses.illinois.edu/cisapp/explorer/schedule/{YEAR}/{SEM}/{classnam[0]}/{classnam[1]}.xml?mode=cascade"
    )
    root = ET.fromstring(r.text)
    sections = root.find("detailedSections")
    coursedict = defaultdict(list)
    for child in sections:
        #print(child.tag, child.attrib, child.text)
        meetings = child.find("meetings")
        if not meetings:
            raise Exception("no meetings")
        meeting = meetings.find("meeting")

        if not meeting:
            raise Exception("no meeting")
        instructors = meeting.find("instructors")
        #print(meeting.tag, meeting.attrib, meeting.text)
        if not instructors:
            classinfo = Classsection(
                child.find("sectionNumber").text,
                child.attrib["id"],
                "None",
                child.find("enrollmentStatus").text,
                meeting.find("start").text,
                meeting.find("end").text,
                meeting.find("daysOfTheWeek").text,
                meeting.find("roomNumber").text
                + " "
                + meeting.find("buildingName").text,
                'None',[], 0,0
            )
            coursedict["None"].append(classinfo)
        else:
            for instructor in instructors:
                name = instructor.text.split(", ")
                a, b = basicinfo(name[0].upper(), name[1].upper())
                c,d = givestats(instructor.text.replace(',','').upper(), boop)
                classinfo = Classsection(
                    child.find("sectionNumber").text,
                    child.attrib["id"],
                    instructor.text,
                    child.find("enrollmentStatus").text,
                    meeting.find("start").text,
                    meeting.find("end").text,
                    meeting.find("daysOfTheWeek").text,
                    meeting.find("roomNumber").text
                    + " "
                    + meeting.find("buildingName").text,a,b,c,d
                )
                coursedict[instructor.text].append(classinfo)
    print(coursedict)


func("MATH 241")
