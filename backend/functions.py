import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from summarize import *
import sqlite3
import ratemyprofessor as rmp
import numpy as np

neededinfo = ["sectionNumber", "CRN", "enrollmentStatus"]

YEAR = 2024
SEM = "fall"
maptf = {True:1, False: -1, None: 0}
mapft = {1 : True, 1 :False, 0:None}
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
        ratings = prof_object.get_ratings(classname.replace(' ',''))
        rmp_nums = np.zeros(4)
        num_ratings = 0
        for rate in ratings:

            arr = np.array([rate.rating, rate.difficulty, rate.take_again,maptf[rate.attendance_mandatory]])
            arr[arr == None] = 0
            print(arr)
            num_ratings+=1
            rmp_nums = rmp_nums + arr


        # if info:
        data = {
        'rating': rmp_nums[0]/num_ratings,
        'difficulty': rmp_nums[1]/num_ratings,
        'take_again': rmp_nums[2]/num_ratings,
        'num_ratings': num_ratings,
        'attendance_mandatory': mapft[round(rmp_nums[3]/num_ratings)],
        }
        prof_info.update(data)
        prof_dict[instructor] = prof_info
    #     else:
    #         rmf_info.append({})
    # #print(info)
    con.close()
    return prof_dict


def func(classname):

    if classname == "ABE 498":
        return "Unsupported class"

    class_name = classname.upper().split() # need courses in CS 222 format
    r = requests.get(
        f"http://courses.illinois.edu/cisapp/explorer/schedule/{YEAR}/{SEM}/{class_name[0]}/{class_name[1]}.xml?mode=cascade"
    )
    print(r.status_code)
    if r.status_code == 404:
       return "not offered next sem"
    if r.status_code != 200:
        return "other error in course api fetching"
    
    coursedict = defaultdict(list)
    profdict = defaultdict(list)
    no_prof = []

    root = ET.fromstring(r.text)
    sections = root.find("detailedSections")
    
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
            no_prof.append(info)
        else:
            for instructor in instructors:
                coursedict[instructor.text].append(info)
    prof_list = list(coursedict.keys())
    
    prof_info = info_lookup(prof_list, classname)
  
    print(coursedict, prof_info)
    return (coursedict, prof_info)


def fetchprof(prof, classname):

    prof_object = rmp.get_professor_by_school_and_name(uni, prof)
    ratings = prof_object.get_ratings(classname.replace(' ','')) 
    if not ratings:
        return "not in ratemyprof"
    need_summary = []
    for rate in ratings:
        if rate.comment:
            need_summary.append(rate.comment)
    print(need_summary)
    # return summarize(need_summary)

#givestats("SOLOMON B", "CS 225")
#fetchprof("VGVhY2hlci0yODczNzI0")