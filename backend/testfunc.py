import functions
import csv
from flask import request
import functions
import sqlite3
from datetime import date

#dictionary of teachers that maps to dictionary of their classes and ave gpa + num students


# with open('./data/gpa.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile, fieldnames=['Year','Term','YearTerm','Subject','Number','Course Title','Sched Type','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','W','Primary Instructor'])
#     for row in reader:
#         if row['Subject'] and row["Number"]:
#             print(row['Subject'], row["Number"])
#             #print(functions.func(row['Subject'] + ' ' + row["Number"]))
#             functions.func(row['Subject'] + ' ' + row["Number"])


def postcomment(course, number):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    #request.form["comment"]
    data = (
    {"course": f'{course} {number}', "comment": "help" ,"time": date.today()}
    )
    cur.execute("INSERT INTO comments VALUES(:course,:comment, :time)", data)
    con.commit()
    params = (f'{course} {number}',)
    cur.execute("SELECT * FROM comments WHERE class = ?", params)
    print(cur.fetchall())
    con.close()

postcomment("CS", 255)
