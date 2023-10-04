import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
# import xlrd


# x = pd.DataFrame()
# print(x)

# data = pd.read_excel('EmployeeSampleData.xlsx')

data = pd.read_excel('EmplolyeeData.xlsx')
column_headers= data.keys().values.tolist()
print(f"Headers of Columns are {column_headers}")

df=data[data['Department'] == "IT"]
print(df)

# conn= mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "omkar")    
# my_cursor = conn.cursor()

# # my_cursor.execute("CREATE TABLE employee (Id INT AUTO_INCREMENT PRIMARY KEY, Emp_id INT NOT NULL, Full_name VARCHAR(55), Job_title VARCHAR(55), Department VARCHAR(55));")

# loc = ()
# a = xlrd.open_workbook("EmployeeSampleData.xlsx")
# sheet = a.sheet_by_index(0)
# sheet.cell_value = (0,0)

# for i in range(1, 21):
#     print(sheet.row_values(i))

# conn.close()




# data = pd.read_excel('EmployeeData.xlsx', nrows=10)

# conn= mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "omkar")    
# my_cursor = conn.cursor()

# table_name = 'emp10'
# schema_definition = '''
#     CREATE TABLE IF NOT EXISTS emp10 (
#     eeid INT,
#     full_name VARCHAR(255),
#     department VARCHAR(255),
#     job_role VARCHAR(255)
# );
# '''
# my_cursor.execute(schema_definition)


# for _, row in data.iterrows():
#     values = tuple(row) 

#     insert_query = f"INSERT INTO {table_name} (eeid, full_name, department, job_role) VALUES ({', '.join(['%s']*len(values))})"
    
   
#     my_cursor.execute(insert_query, values)


# conn.commit()
# conn.close()

# print('Data successfully inserted into the MySQL database.')
