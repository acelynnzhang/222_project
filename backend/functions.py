import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from summarize import *
import sqlite3
import ratemyprofessor as rmp
from statistics import mean
from datetime import date

neededinfo = ["sectionNumber", "CRN", "enrollmentStatus"]

YEAR = 2024
SEM = "fall"
uni = rmp.get_school_by_name("University of Illinois Urbana-Champaign")

def info_lookup(instructors,classname):
    
    print(instructors,classname)
    con = sqlite3.connect("gpa.db")
    cur = con.cursor()
    prof_dict ={}
    for instructor in instructors:
        prof_info = {}
        print(instructor.upper().replace(',', ''))
        params = (classname,instructor.replace(',', ''),)
        print(cur.execute("SELECT avegpa,pastnumstudents FROM gpa WHERE class = ? AND prof = ?", params).fetchall())
        csv_results = cur.execute("SELECT avegpa,pastnumstudents FROM gpa WHERE class = ? AND prof = ?", params).fetchall()
        
        # prof_info['ave_gpa'] = csv_results[0]
        # prof_info['ave_gpa'] = csv_results[1]
        prof_object = rmp.get_professor_by_school_and_name(uni, instructor)
        print(prof_object)
        if prof_object:
            print(prof_object)
            ratings = prof_object.get_ratings(classname.replace(' ',''))
            if not ratings:
                ratings = prof_object.get_ratings(classname.lower().replace(' ','').capitalize())
                print(classname.lower().replace(' ','').capitalize())
            num_ratings = 0
            if ratings:
                data = {
                'rating': mean([rating.rating for rating in ratings]),
                'difficulty': mean([rating.difficulty for rating in ratings]),
                'take_again': mean([rating.take_again for rating in ratings if rating.take_again is not None]),
                'num_ratings': len(ratings),
                'attendance_mandatory': mean([rating.attendance_mandatory for rating in ratings if rating.attendance_mandatory is not None]),
                }
                prof_info.update(data)
        prof_dict[instructor] = prof_info
    con.close()
    return prof_dict


def class_info(classname):
    class_name = classname.upper().split() # need courses in CS 222 format

    if class_name[1] == "498":
        return "Unsupported class"

    r = requests.get(
        f"http://courses.illinois.edu/cisapp/explorer/schedule/{YEAR}/{SEM}/{class_name[0]}/{class_name[1]}.xml?mode=cascade"
    )
    print(r.status_code)
    if r.status_code == 404:
       return None, None
    if r.status_code != 200:
        return "Other error in course API", None
    
    coursedict = defaultdict(list)
    profdict = defaultdict(list)
    no_prof = []

    root = ET.fromstring(r.text)
    sections = root.find("detailedSections")
    
    for child in sections:
        #print(child.tag, child.attrib, child.text)
        meetings = child.find("meetings")
        if not meetings:
            return "Other error in course API", None
        meeting = meetings.find("meeting")

        if not meeting:
            return "Other error in course API", None
        
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
            no_prof.append(info)
        else:
            for instructor in instructors:
                coursedict[instructor.text].append(info)
    prof_list = list(coursedict.keys())
    
    prof_info = info_lookup(prof_list, classname)
  
    print(coursedict, prof_info)
    return (coursedict, prof_info)


def fetch_prof(prof, classname):

    prof_object = rmp.get_professor_by_school_and_name(uni, prof)
    if classname:
        classname = classname.replace(' ','')
    ratings = prof_object.get_ratings(classname)
    if not ratings:
        return None
    need_summary = []
    for rate in ratings:
        if rate.comment:
            need_summary.append(rate.comment)
    print(need_summary)
    return summarize(need_summary)

# fetch_prof("SOLOMON B", "CS 225")
#fetchprof("VGVhY2hlci0yODczNzI0")

def add_comment(course, number, comment):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    data = (
    {"course": f'{course} {number}', "comment": comment ,"time": date.today()}
    )
    cur.execute("INSERT INTO comments VALUES(:course,:comment, :time)", data)
    con.commit()
    con.close()


def fetch_comments(course, number):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    params = (f'{course} {number}',)
    cur.execute("SELECT comment,dateposted FROM comments WHERE class = ?", params)
    comments = cur.fetchall()
    print(comments)
    con.close()
    return comments

