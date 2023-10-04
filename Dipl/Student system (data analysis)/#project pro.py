#project pro 
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

config = {
    "user": "root",
    "password": "root@123",
    "host": "localhost",
    "database": "seqr_d_icat",
}
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

student_table = "student_table"  
cursor.execute(f"SELECT * FROM {student_table}")
data = cursor.fetchall()

column_names = ["id", "serial_no", "student_name", "certificate_file", "template_id", "key", "path", "created_by",
                "updated_by", "status", "publish", "scan_count", "site_id", "template_type", "bc_txn_hash",
                "created_at", "updated_at"]  # Replace with your actual column names
df = pd.DataFrame(data, columns=column_names)

while True:
    # Input for desired starting year and month
    start_year = int(input("Enter the starting year (e.g., 2022): "))
    start_month = int(input("Enter the starting month (e.g., 1 for January): "))

    # Input for desired ending year and month
    end_year = int(input("Enter the ending year (e.g., 2022): "))
    end_month = int(input("Enter the ending month (e.g., 12 for December): "))

    # Filter the DataFrame based on user input
    filtered_df = df[
        (df['created_at'].dt.year >= start_year) & (df['created_at'].dt.year <= end_year) &
        (df['created_at'].dt.month >= start_month) & (df['created_at'].dt.month <= end_month)
    ]

    count_0s = len(filtered_df[filtered_df['status'] == 1])
    count_1s = len(filtered_df[filtered_df['status'] == 2])

    print(f'Number of active users from {start_month}/{start_year} to {end_month}/{end_year}: {count_1s}')
    print(f'Number of non-active users from {start_month}/{start_year} to {end_month}/{end_year}: {count_0s}')

    # Pie chart for user status
    active_users = f"{count_1s}"
    non_active_users = f"{count_0s}"

    sizes = [active_users, non_active_users]
    labels = ['Active Users', 'Non-Active Users']
    colors = ['green', 'red']

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('User Activity')
    plt.show()
# Ask the user if they want to continue
    continue_input = input("Do you want to continue (yes/no)? ").lower()
    if continue_input != 'yes':
        break 
    
while True:
    # Input for desired year and month for marksheets printed
    desired_year = int(input("Enter the desired year (e.g., 2022): "))
    desired_month = int(input("Enter the desired month (e.g., 1 for January): "))

    # Filter the DataFrame based on user input for marksheets printed
    filtered_df = df[(df['created_at'].dt.year == desired_year) & (df['created_at'].dt.month == desired_month)]
    total_entries = len(filtered_df)
    print(f"Total entries in {desired_month}/{desired_year}: {total_entries}")

    # Total marksheets printed in the selected year and month
    marksheets_printed = f"{desired_month}/{desired_year}:{total_entries}"
    marksheets_printed = int(marksheets_printed.split(":")[1])

    # Pie chart for marksheets printed
    sizes = [marksheets_printed, total_entries - marksheets_printed]
    labels = [f"Marksheets printed in {desired_month}/{desired_year}",
              f"Other entries in {desired_month}/{desired_year}"]
    colors = ['pink', 'purple']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Marksheets Printed')
    plt.show()

    # Ask the user if they want to continue
    continue_input = input("Do you want to continue (yes/no)? ").lower()
    if continue_input != 'yes':
        break

cursor.close()
conn.close()
    