import functions
import csv
#dictionary of teachers that maps to dictionary of their classes and ave gpa + num students


with open('./data/gpa.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['Year','Term','YearTerm','Subject','Number','Course Title','Sched Type','A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','W','Primary Instructor'])
    for row in reader:
        if row['Subject'] and row["Number"]:
            print(row['Subject'], row["Number"])
            print(functions.func(row['Subject'] + ' ' + row["Number"]))
