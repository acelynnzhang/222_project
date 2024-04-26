from collections import defaultdict
import csv, sqlite3
from typing import Dict

gpadict = defaultdict(lambda: defaultdict())
#dictionary of teachers that maps to dictionary of their classes and ave gpa + num students

GRADE_MAPPING: Dict[str, float] = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.67,
    "B+" : 3.33,
    "B" : 3.0,
    "B-": 2.67,
    "C+": 2.33,
    "C": 2.0,
    "C-":1.67,
    "D+":1.33,
    "D":1.0,
    "D-": 0.67
}

with open('./data/gpa.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['Year','Term','YearTerm','Subject','Number','Course Title','Sched Type','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','W','Primary Instructor'])
    for row in reader:
        if row['Primary Instructor']:
            prof = row['Primary Instructor'].upper().split(', ')
            prof = f'{prof[0]} {prof[1][0]}'
            tot_num = 0.0
            sum_points = 0.0
            for grade in GRADE_MAPPING:
                tot_num += int(row[grade])  
                sum_points += int(row[grade]) * GRADE_MAPPING[grade]
            classnum = f'{row["Subject"]} {row["Number"]}'
            if classnum  in gpadict[prof]:
                gpadict[prof][classnum ]['sumtot'] += sum_points
                gpadict[prof][classnum ]['sumstudents'] += tot_num
            else:
                gpadict[prof][classnum ] = {'sumtot':sum_points, 'sumstudents':tot_num}
            



con = sqlite3.connect("gpa.db")
cur = con.cursor()
cur.execute("CREATE TABLE geepa(class,prof, avegpa, pastnumstudents)")
for prof in gpadict:
    for classtaught in gpadict[prof]:
        data = (
        {"course": classtaught , "prof": prof , "avegpa": gpadict[prof][classtaught]['sumtot']/gpadict[prof][classtaught]['sumstudents'], "pastnumstudents":gpadict[prof][classtaught]['sumstudents']}
        )
        cur.execute("INSERT INTO gpa VALUES(:course,:prof, :avegpa, :pastnumstudents)", data)
        con.commit()

con.close()