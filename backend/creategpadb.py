import csv, sqlite3

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


con = sqlite3.connect("gpa.db")
cur = con.cursor()
cur.execute("CREATE TABLE gpa(class,prof, avegpa, pastnumstudents)")
for prof in gpadict:
    for classtaught in gpadict[prof]:
        data = (
        {"course": classtaught , "prof": prof , "avegpa": gpadict[prof][classtaught]['sumtot']/gpadict[prof][classtaught]['sumstudents'], "pastnumstudents":gpadict[prof][classtaught]['sumstudents']}
        )
        cur.execute("INSERT INTO gpa VALUES(:course,:prof, :avegpa, :pastnumstudents)", data)
        con.commit()

con.close()