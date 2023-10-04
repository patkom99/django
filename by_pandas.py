import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database= "omkar"
)
my_cursor = conn.cursor()

# my_cursor.execute('CREATE TABLE Emp_data_101(Emp_id VARCHAR(25), Full_name VARCHAR(255), Job_title VARCHAR(255), Department VARCHAR(255))')
# my_cursor.close()

data = pd.read_excel("EmplolyeeData.xlsx")
print(data)

for index, row in data.iterrows():
    # print(index)
    Emp_id = row['EEID']
    Full_name = row['Full Name']
    Job_title = row['Job Title']
    Department = row['Department'] 
    sql = "INSERT INTO emp_data_101(Emp_id, Full_name, Job_title, Department) VALUES(%s, %s, %s, %s)"
    val=(Emp_id, Full_name, Job_title, Department)
    my_cursor.execute(sql, val)

conn.commit()

my_cursor.close()
conn.close()