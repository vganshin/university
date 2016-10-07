
# coding: utf-8

# In[32]:

import csv

raw_data = open("marks.csv")
students = csv.reader(raw_data)

def average(marks):
    return str(float(reduce(lambda a, b: a + b, map(int, marks))) / len(marks))

groups = {}

for student in students:
    group = student[1]
    marks = student[2:]
    avg = average(marks)
    
    if not groups.get(group):
        groups[group] = []
    
    student[1] = average(marks)
    
    record = " ".join(student)
    
    groups[group].append(record)
    
for group, students in groups.items():
    print("Группа {group}:".format(group=group))
    for student in students:
        print(student)

