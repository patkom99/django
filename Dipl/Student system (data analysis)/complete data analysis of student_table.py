import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

# Database configuration
db_config = {
    "user": "root",
    "password": "root@123",
    "host": "localhost",
    "database": "seqr_d_icat",
}

# Function to fetch data from the database
def fetch_data(table_name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()
    return data

# Create a Tkinter window
root = tk.Tk()
root.title("Data Analysis Tool")

# Function to perform data analysis for user status
def perform_user_status_analysis():
    # Get the selected start and end dates from DateEntry widgets
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()

    # Convert date to datetime for comparison
    start_datetime = datetime.datetime.strptime(start_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
    end_datetime = datetime.datetime.strptime(end_date.strftime('%d/%m/%Y'), '%d/%m/%Y')

    # Fetch data from the database (you can modify this query as needed)
    student_data = fetch_data("student_table")
    column_names = ["id", "serial_no", "student_name", "certificate_file", "template_id", "key", "path", "created_by",
                    "updated_by", "status", "publish", "scan_count", "site_id", "template_type", "bc_txn_hash",
                    "created_at", "updated_at"]
    df = pd.DataFrame(student_data, columns=column_names)

    # Filter data based on user input
    filtered_df = df[
        (df['created_at'] >= start_datetime) & (df['created_at'] <= end_datetime)
    ]

    # Calculate the count of active and non-active users
    count_0s = len(filtered_df[filtered_df['status'] == 1])
    count_1s = len(filtered_df[filtered_df['status'] == 2])

    # Update the user status label
    user_status_label.config(text=f'Number of active users: {count_1s}\nNumber of non-active users: {count_0s}')

    # Pie chart for user status
    active_users = count_1s
    non_active_users = count_0s

    sizes = [active_users, non_active_users]
    labels = [f'Active Users ({count_1s})', f'Non-Active Users ({count_0s})']
    colors = ['green', 'red']

    # Clear the previous chart
    user_status_ax.clear()

    # Plot the pie chart for user status
    user_status_ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    user_status_ax.axis('equal')
    user_status_ax.set_title('User Activity')

    # Update the user status canvas
    user_status_canvas.draw()

# Function to perform data analysis for marksheets
def perform_marksheets_analysis():
    # Get the selected start and end dates from DateEntry widgets
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()

    # Convert date to datetime for comparison
    start_datetime = datetime.datetime.strptime(start_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
    end_datetime = datetime.datetime.strptime(end_date.strftime('%d/%m/%Y'), '%d/%m/%Y')

    # Fetch data from the database (you can modify this query as needed)
    marksheets_data = fetch_data("student_table")
    marksheets_column_names = ["id", "serial_no", "student_name", "certificate_file", "template_id", "key", "path", "created_by",
                    "updated_by", "status", "publish", "scan_count", "site_id", "template_type", "bc_txn_hash",
                    "created_at", "updated_at"]
    marksheets_df = pd.DataFrame(marksheets_data, columns=marksheets_column_names)

    # Filter marksheets data based on user input
    filtered_marksheets_df = marksheets_df[
        (marksheets_df['created_at'] >= start_datetime) & (marksheets_df['created_at'] <= end_datetime)
    ]

    # Calculate the total number of marksheets printed ever
    total_marksheets_ever = len(filtered_marksheets_df)

    # Update the marksheets label
    marksheets_label.config(text=f'Total marksheets printed in this time frame: {total_marksheets_ever}')

    # Pie chart for marksheets
    marksheets_printed = total_marksheets_ever
    other_entries = len(marksheets_df) - total_marksheets_ever

    sizes = [marksheets_printed, other_entries]
    labels = [f'Marksheets Printed ({marksheets_printed})', f'Other Entries ({other_entries})']
    colors = ['pink', 'purple']

    # Clear the previous chart
    marksheets_ax.clear()

    # Plot the pie chart for marksheets
    marksheets_ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=180)
    marksheets_ax.axis('equal')
    marksheets_ax.set_title('Marksheets Printed')

    # Update the marksheets canvas
    marksheets_canvas.draw()

# Create labels and DateEntry widgets for date input
start_date_label = ttk.Label(root, text="From (dd/mm/yyyy):")
start_date_label.grid(row=0, column=0, padx=10, pady=10)
start_date_entry = DateEntry(root, width=12, date_pattern='dd/mm/yyyy')
start_date_entry.grid(row=0, column=1, padx=10, pady=10)
end_date_label = ttk.Label(root, text="To (dd/mm/yyyy):")
end_date_label.grid(row=1, column=0, padx=10, pady=10)
end_date_entry = DateEntry(root, width=12, date_pattern='dd/mm/yyyy')
end_date_entry.grid(row=1, column=1, padx=10, pady=10)

# Create buttons to trigger data analysis
user_status_button = ttk.Button(root, text="Analyze User Status", command=perform_user_status_analysis)
user_status_button.grid(row=2, column=0, padx=10, pady=10)
marksheets_button = ttk.Button(root, text="Analyze Marksheets", command=perform_marksheets_analysis)
marksheets_button.grid(row=2, column=1, padx=10, pady=10)

# Create Matplotlib figures to display charts
user_status_fig, user_status_ax = plt.subplots(figsize=(4, 4))
marksheets_fig, marksheets_ax = plt.subplots(figsize=(4, 4))

# Create canvas widgets for Matplotlib figures
user_status_canvas = FigureCanvasTkAgg(user_status_fig, master=root)
user_status_canvas.get_tk_widget().grid(row=3, column=0, padx=10, pady=10)
marksheets_canvas = FigureCanvasTkAgg(marksheets_fig, master=root)
marksheets_canvas.get_tk_widget().grid(row=3, column=1, padx=10, pady=10)

# Create labels to display the analysis results
user_status_label = ttk.Label(root, text="")
user_status_label.grid(row=4, column=0, padx=10, pady=10)
marksheets_label = ttk.Label(root, text="")
marksheets_label.grid(row=4, column=1, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()