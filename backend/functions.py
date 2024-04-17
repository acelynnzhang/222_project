import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from summarize import *
import sqlite3


neededinfo = ["sectionNumber", "CRN", "enrollmentStatus"]

YEAR = 2024
SEM = "fall"


def givestats(instructor,classname):
    # a = 0
    # b = 0
    # print(instructor,classname)
    con = sqlite3.connect("gpa.db")
    cur = con.cursor()
    params = (classname,instructor,)
    info = cur.execute("SELECT avegpa,pastnumstudents FROM gpa WHERE class = ? AND prof = ?", params).fetchall()
    #print(info)
    con.close()
    return info
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
    if response.status_code != 200:
        return "None", "None"
    r = response.json()
    for thing in r["data"]["newSearch"]["teachers"]["edges"]:
        if (
            thing["node"]["lastName"].upper() == lastname
            and thing["node"]["firstName"][0].upper() == firstletter
        ):
            mandatoryAttendance = None
            currval = 0
            for key in thing["node"]["mandatoryAttendance"]:
                if (
                    key != "total"
                    and thing["node"]["mandatoryAttendance"][key] > currval
                ):
                    mandatoryAttendance = key
                    currval = thing["node"]["mandatoryAttendance"][key]
            return (
                thing["node"]["id"],
                [
                    thing["node"]["avgRating"],
                    mandatoryAttendance,
                    thing["node"]["ratingsDistribution"]["total"],
                    thing["node"]["wouldTakeAgainPercentRounded"],
                ]
            )

    return "None", "None"


def func(classname):

    if classname == "ABE 498":
        return "nah"

    classnam = classname.upper()
    classnam = classnam.split()  # need courses in CS 222 format
    r = requests.get(
        f"http://courses.illinois.edu/cisapp/explorer/schedule/{YEAR}/{SEM}/{classnam[0]}/{classnam[1]}.xml?mode=cascade"
    )
    print(r.status_code)
    if r.status_code == 404:
       return "not offered next sem"
    if r.status_code != 200:
        return "other error in course api fetching"
    root = ET.fromstring(r.text)
    sections = root.find("detailedSections")
    coursedict = defaultdict(list)
    profdict = defaultdict(list)
    for child in sections:
        #print(child.tag, child.attrib, child.text)
        meetings = child.find("meetings")
        if not meetings:
            raise Exception("no meetings")
        meeting = meetings.find("meeting")

        if not meeting:
            raise Exception("no meeting")
        
        #info = [child.find("sectionNumber").text, child.attrib["id"], child.find("enrollmentStatus").text]
        info = []

        for entry in neededinfo:
            if entry == "CRN":
                if child.attrib["id"]:
                    info.append(child.attrib["id"])
            elif not child.find(entry).text:
                info.append(None)
            else:
                info.append(child.find(entry).text)


        instructors = meeting.find("instructors")
            
        #print(meeting.tag, meeting.attrib, meeting.text)
        if not instructors:
            coursedict["None"].append(info)
        else:
            for instructor in instructors:
                coursedict[instructor.text].append(info)
                if instructor.text not in profdict:
                    name = instructor.text.split(", ")
                    a,b = basicinfo(name[0].upper(), name[1].upper())
                    profdict[instructor.text] = [a,b,givestats(instructor.text.replace(',','').upper(), classname)]
    print(coursedict, profdict)
    return coursedict, profdict


def fetchprof(id):

    headers = {
        "Authorization": "Basic dGVzdDp0ZXN0"
    }

    json_data = {
        "query": "query TeacherRatingsPageQuery(\n  $id: ID!\n) {\n  node(id: $id) {\n    __typename\n    ... on Teacher {\n      id\n      legacyId\n      firstName\n      lastName\n      department\n      school {\n        legacyId\n        name\n        city\n        state\n        country\n        id\n      }\n      lockStatus\n      ...StickyHeader_teacher\n      ...RatingDistributionWrapper_teacher\n      ...TeacherInfo_teacher\n      ...SimilarProfessors_teacher\n      ...TeacherRatingTabs_teacher\n    }\n    id\n  }\n}\n\nfragment StickyHeader_teacher on Teacher {\n  ...HeaderDescription_teacher\n  ...HeaderRateButton_teacher\n}\n\nfragment RatingDistributionWrapper_teacher on Teacher {\n  ...NoRatingsArea_teacher\n  ratingsDistribution {\n    total\n    ...RatingDistributionChart_ratingsDistribution\n  }\n}\n\nfragment TeacherInfo_teacher on Teacher {\n  id\n  lastName\n  numRatings\n  ...RatingValue_teacher\n  ...NameTitle_teacher\n  ...TeacherTags_teacher\n  ...NameLink_teacher\n  ...TeacherFeedback_teacher\n  ...RateTeacherLink_teacher\n  ...CompareProfessorLink_teacher\n}\n\nfragment SimilarProfessors_teacher on Teacher {\n  department\n  relatedTeachers {\n    legacyId\n    ...SimilarProfessorListItem_teacher\n    id\n  }\n}\n\nfragment TeacherRatingTabs_teacher on Teacher {\n  numRatings\n  courseCodes {\n    courseName\n    courseCount\n  }\n  ...RatingsList_teacher\n  ...RatingsFilter_teacher\n}\n\nfragment RatingsList_teacher on Teacher {\n  id\n  legacyId\n  lastName\n  numRatings\n  school {\n    id\n    legacyId\n    name\n    city\n    state\n    avgRating\n    numRatings\n  }\n  ...Rating_teacher\n  ...NoRatingsArea_teacher\n  ratings(first: 20) {\n    edges {\n      cursor\n      node {\n        ...Rating_rating\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n  }\n}\n\nfragment RatingsFilter_teacher on Teacher {\n  courseCodes {\n    courseCount\n    courseName\n  }\n}\n\nfragment Rating_teacher on Teacher {\n  ...RatingFooter_teacher\n  ...RatingSuperHeader_teacher\n  ...ProfessorNoteSection_teacher\n}\n\nfragment NoRatingsArea_teacher on Teacher {\n  lastName\n  ...RateTeacherLink_teacher\n}\n\nfragment Rating_rating on Rating {\n  comment\n  flagStatus\n  createdByUser\n  teacherNote {\n    id\n  }\n  ...RatingHeader_rating\n  ...RatingSuperHeader_rating\n  ...RatingValues_rating\n  ...CourseMeta_rating\n  ...RatingTags_rating\n  ...RatingFooter_rating\n  ...ProfessorNoteSection_rating\n}\n\nfragment RatingHeader_rating on Rating {\n  legacyId\n  date\n  class\n  helpfulRating\n  clarityRating\n  isForOnlineClass\n}\n\nfragment RatingSuperHeader_rating on Rating {\n  legacyId\n}\n\nfragment RatingValues_rating on Rating {\n  helpfulRating\n  clarityRating\n  difficultyRating\n}\n\nfragment CourseMeta_rating on Rating {\n  attendanceMandatory\n  wouldTakeAgain\n  grade\n  textbookUse\n  isForOnlineClass\n  isForCredit\n}\n\nfragment RatingTags_rating on Rating {\n  ratingTags\n}\n\nfragment RatingFooter_rating on Rating {\n  id\n  comment\n  adminReviewedAt\n  flagStatus\n  legacyId\n  thumbsUpTotal\n  thumbsDownTotal\n  thumbs {\n    thumbsUp\n    thumbsDown\n    computerId\n    id\n  }\n  teacherNote {\n    id\n  }\n  ...Thumbs_rating\n}\n\nfragment ProfessorNoteSection_rating on Rating {\n  teacherNote {\n    ...ProfessorNote_note\n    id\n  }\n  ...ProfessorNoteEditor_rating\n}\n\nfragment ProfessorNote_note on TeacherNotes {\n  comment\n  ...ProfessorNoteHeader_note\n  ...ProfessorNoteFooter_note\n}\n\nfragment ProfessorNoteEditor_rating on Rating {\n  id\n  legacyId\n  class\n  teacherNote {\n    id\n    teacherId\n    comment\n  }\n}\n\nfragment ProfessorNoteHeader_note on TeacherNotes {\n  createdAt\n  updatedAt\n}\n\nfragment ProfessorNoteFooter_note on TeacherNotes {\n  legacyId\n  flagStatus\n}\n\nfragment Thumbs_rating on Rating {\n  id\n  comment\n  adminReviewedAt\n  flagStatus\n  legacyId\n  thumbsUpTotal\n  thumbsDownTotal\n  thumbs {\n    computerId\n    thumbsUp\n    thumbsDown\n    id\n  }\n  teacherNote {\n    id\n  }\n}\n\nfragment RateTeacherLink_teacher on Teacher {\n  legacyId\n  numRatings\n  lockStatus\n}\n\nfragment RatingFooter_teacher on Teacher {\n  id\n  legacyId\n  lockStatus\n  isProfCurrentUser\n  ...Thumbs_teacher\n}\n\nfragment RatingSuperHeader_teacher on Teacher {\n  firstName\n  lastName\n  legacyId\n  school {\n    name\n    id\n  }\n}\n\nfragment ProfessorNoteSection_teacher on Teacher {\n  ...ProfessorNote_teacher\n  ...ProfessorNoteEditor_teacher\n}\n\nfragment ProfessorNote_teacher on Teacher {\n  ...ProfessorNoteHeader_teacher\n  ...ProfessorNoteFooter_teacher\n}\n\nfragment ProfessorNoteEditor_teacher on Teacher {\n  id\n}\n\nfragment ProfessorNoteHeader_teacher on Teacher {\n  lastName\n}\n\nfragment ProfessorNoteFooter_teacher on Teacher {\n  legacyId\n  isProfCurrentUser\n}\n\nfragment Thumbs_teacher on Teacher {\n  id\n  legacyId\n  lockStatus\n  isProfCurrentUser\n}\n\nfragment SimilarProfessorListItem_teacher on RelatedTeacher {\n  legacyId\n  firstName\n  lastName\n  avgRating\n}\n\nfragment RatingValue_teacher on Teacher {\n  avgRating\n  numRatings\n  ...NumRatingsLink_teacher\n}\n\nfragment NameTitle_teacher on Teacher {\n  id\n  firstName\n  lastName\n  department\n  school {\n    legacyId\n    name\n    id\n  }\n  ...TeacherDepartment_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment TeacherTags_teacher on Teacher {\n  lastName\n  teacherRatingTags {\n    legacyId\n    tagCount\n    tagName\n    id\n  }\n}\n\nfragment NameLink_teacher on Teacher {\n  isProfCurrentUser\n  id\n  legacyId\n  firstName\n  lastName\n  school {\n    name\n    id\n  }\n}\n\nfragment TeacherFeedback_teacher on Teacher {\n  numRatings\n  avgDifficulty\n  wouldTakeAgainPercent\n}\n\nfragment CompareProfessorLink_teacher on Teacher {\n  legacyId\n}\n\nfragment TeacherDepartment_teacher on Teacher {\n  department\n  departmentId\n  school {\n    legacyId\n    name\n    id\n  }\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n\nfragment NumRatingsLink_teacher on Teacher {\n  numRatings\n  ...RateTeacherLink_teacher\n}\n\nfragment RatingDistributionChart_ratingsDistribution on ratingsDistribution {\n  r1\n  r2\n  r3\n  r4\n  r5\n}\n\nfragment HeaderDescription_teacher on Teacher {\n  id\n  firstName\n  lastName\n  department\n  school {\n    legacyId\n    name\n    city\n    state\n    id\n  }\n  ...TeacherTitles_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment HeaderRateButton_teacher on Teacher {\n  ...RateTeacherLink_teacher\n}\n\nfragment TeacherTitles_teacher on Teacher {\n  department\n  school {\n    legacyId\n    name\n    id\n  }\n}\n",
        "variables": {
            "id": id,
        },
    }

    response = requests.post(
        "https://www.ratemyprofessors.com/graphql",
        headers=headers,
        json=json_data,
    )
    if response.status_code != 200:
        return "not in ratemyprof"
    print(response.text)

    print("ok")
    return summarize(response.text)

#givestats("SOLOMON B", "CS 225")
#fetchprof("VGVhY2hlci0yODczNzI0")