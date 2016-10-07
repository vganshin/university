
# coding: utf-8

# In[13]:

import csv

raw_data = open("marks.csv")
students = csv.reader(raw_data)

def average(marks):
    return sum([float(mark) for mark in marks]) / len(marks)

groups = {}

for student in students:
    group = student[1]
    marks = student[2:]
    avg = average(marks)
    
    if not groups.get(group):
        groups[group] = []
    
    student[1] = average(marks)
    
    
    
    groups[group].append(student)
    
for group, students in groups.items():
    print("Группа {group}:".format(group=group))
    
    students = sorted(students, key = lambda x: x[1], reverse=True)
    
    for student in students:
        print("{} {} {}".format(student[0], student[1], " ".join(student[2:])))

