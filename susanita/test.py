
#!/usr/bin/python


import pdfplumber
import pandas as pd
from math import floor


filename = "12.pdf"
outputname = "12.xlsx"

all_text = []
all_tables = []

student_names = []
assignments = []
comments = {}

with pdfplumber.open(filename) as pdf:
    for page in pdf.pages:
        all_tables.append(page.extract_tables())
        all_text.append(page.extract_text())


number_of_pages = len(all_tables)
number_of_students = floor(number_of_pages/2)

for student in range(number_of_students):
    name_index = 2*student
    table_index = 2*student+1
    L = all_text[name_index].find("\n")
    name_of_this_student = all_text[name_index][:L]
    student_names.append(name_of_this_student)
    comments[name_of_this_student] = {}
    student_report = all_tables[table_index]
    length_of_report = len(student_report[0])
    for assignment in range(length_of_report):
        entry = student_report[0][assignment][1]
        L = entry.find(":")
        assignment_name = entry[:L]
        if assignment_name not in assignments:
            assignments.append(assignment_name)
        if len(student_report[0][assignment][1][L+1:]) > 1:
            comment = student_report[0][assignment][1][L+2:]
        else:
            comment = ""
        comments[name_of_this_student][assignment_name] = comment

data = {}

data["Names"] = student_names

for assignment in assignments:
    data[assignment] = []
    for student in student_names:
        if assignment in comments[student]:
            data[assignment].append(comments[student][assignment])
        else:
            data[assignment].append("")

df = pd.DataFrame(data)
df.to_excel(outputname,index=False)
