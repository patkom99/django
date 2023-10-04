import pandas as pd
import mysql.connector

conn= mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "omkar")    
my_cursor = conn.cursor()

import csv 
filename="EmplolyeeData.csv"

with open(filename,"r") as csvfile:
    csvreader = csv.reader(csvfile)
    neglect = next(csvreader)

    for row in csvreader:
        Emp_id = row[0]
        Full_name = row[1]
        Job_title = row[2]
        Department = row[3] 
        sql = "insert into employee(Emp_id, Full_name, Job_title, Department) VALUES(%s, %s, %s, %s)"
        val=(Emp_id, Full_name, Job_title, Department)
        my_cursor.execute(sql, val)

conn.commit()