import mysql.connector
import tkinter as tk
from tkinter import END, Text, ttk, messagebox
from tkcalendar import DateEntry

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root@123",
    "database": "dipl_system",
}

# Function to fetch data from the database
def fetch_data(start_date, end_date, selected_columns_str):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Construct the SQL query based on user input
        query = f"SELECT {selected_columns_str} FROM purchase_documents WHERE doc_date BETWEEN %s AND %s"

        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()

        conn.close()
        return data

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")
        return []

# Function to show details when an ID is clicked
def show_detail(event):
    item = result_treeview.selection()[0]  # Get the selected item in result_treeview
    id_value = result_treeview.item(item, "values")[0]  # Get the id from the selected item

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Construct the SQL query to fetch all data for the selected id
        query = """
        SELECT pd.*, pm.name
        FROM purchase_documents AS pd
        LEFT JOIN party_masters pm ON pd.party_id = pm.id
        WHERE pd.id = %s
        """
        cursor.execute(query, (id_value,))
        data = cursor.fetchall()

        conn.close()

        # Clear existing data in the detail_treeview
        for item in detail_treeview.get_children():
            detail_treeview.delete(item)

        # Display the details in the detail_treeview
        for row in data:
            detail_treeview.insert("", "end", values=row)

        # Update the vertical_treeview with the selected data
        update_vertical_columns(data)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")

# Function to handle the "Show Data" button click event
def show_data():
    global current_page
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    selected_columns = [col for col, var in zip(available_columns, column_vars) if var.get() == "1"]

    if not start_date or not end_date:
        messagebox.showerror("Error", "Please enter start and end dates.")
        return

    selected_columns_str = ", ".join(selected_columns)
    selected_columns_str = "id,doc_number, doc_date, total_amount, product_category"

    # Calculate the offset based on the current page
    offset = (current_page - 1) * items_per_page

    data = fetch_data(start_date, end_date, selected_columns_str)

    if data:
        # Clear existing data in the treeview
        for item in result_treeview.get_children():
            result_treeview.delete(item)

        # Display only the data for the current page
        for row in data[offset:offset + items_per_page]:
            result_treeview.insert("", "end", values=row)

    else:
        messagebox.showinfo("No Data", "No data found for the specified date range.")

# Function to go to the next page
def next_page():
    global current_page
    current_page += 1
    show_data()

# Function to go to the previous page
def previous_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        show_data()

# Create the main window
root = tk.Tk()
root.title("Database Query Tool")

# Labels and date pickers for date range using tkcalendar
start_date_label = ttk.Label(root, text="Start Date:")
start_date_label.grid(row=0, column=0, padx=10, pady=(10, 0))  # Adjust the padx and pady values

start_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd")
start_date_entry.grid(row=0, column=1, padx=10, pady=(10, 0))  # Adjust the padx and pady values

end_date_label = ttk.Label(root, text="End Date:")
end_date_label.grid(row=1, column=0, padx=10)

end_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd")
end_date_entry.grid(row=1, column=1, padx=10)

available_columns = ["id", "doc_number", "doc_date", "total_amount", "product_category"]  # Replace with your actual column names
column_vars = []

# Button to fetch and display data
show_button = ttk.Button(root, text="Show Data", command=show_data)
show_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Create a Treeview widget for displaying data in a table
result_treeview = ttk.Treeview(root, columns=available_columns, show="headings", height=7)

# Configure column headings
for col in available_columns:
    result_treeview.heading(col, text=col)
    result_treeview.column(col, width=250)  # Adjust the width as needed

result_treeview.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

# Add navigation buttons for next and previous pages
next_button = ttk.Button(root, text="Next Page", command=next_page)
next_button.grid(row=5, column=0, padx=10, pady=10)

previous_button = ttk.Button(root, text="Previous Page", command=previous_page)
previous_button.grid(row=5, column=1, padx=10, pady=10)

# Initialize current_page and items_per_page
current_page = 1
items_per_page = 10

# Bind double-click event to the id column
result_treeview.bind("<Double-1>", show_detail)

# Update the available_columns_detail list with the new column names
available_columns_detail = [
    "ID", "DOCUMENT_NO", "DOCUMENT_DATE", "PARTY_ID", "PRODUCT_DETAILS", "TOATAL_AMOUNT",
    "PRODUCT_CATEGORY", "DESCRIPTION", "THREAD_SUPPLIER", "COMPANY_ID",
    "CHECKLIST_IDS",  "PDF_FILE", "PD_LOCATION", "REFERENCE_NO", "REFERENCE_SR",  # Add the new column name here
    "STATUS", "CREATED_BY", "CREATED_AT", "UPDATED_AT", "NAME"
]

# Create a new Treeview widget for displaying details with a reduced height
detail_treeview = ttk.Treeview(root, columns=available_columns_detail, show="headings", height=2)

# Configure column headings with the updated column names
for col in available_columns_detail:
    detail_treeview.heading(col, text=col)
    detail_treeview.column(col, width=65)  # Adjust the width as needed

detail_treeview.grid(row=6, column=0, columnspan=2, padx=20, pady=20)


# Create a frame for the vertical Treeview and labels
vertical_frame = ttk.Frame(root)
vertical_frame.grid(row=8, column=1, padx=20, pady=20, sticky="nsew")

# Create a vertical scrollbar for the vertical Treeview
vertical_scrollbar_detail = ttk.Scrollbar(vertical_frame, orient="vertical")
vertical_scrollbar_detail.grid(row=0, column=1, sticky="ns")

# Create horizontal scrollbar for the vertical Treeview
horizontal_scrollbar_detail = ttk.Scrollbar(vertical_frame, orient="horizontal")
horizontal_scrollbar_detail.grid(row=7, column=0, sticky="ns")

# Create a vertical Treeview widget for displaying details
vertical_treeview = ttk.Treeview(vertical_frame, columns=["Property", "Value"], show="headings", height=10)
vertical_treeview.grid(row=0, column=0)

# Configure column headings for the vertical Treeview
vertical_treeview.heading("Property", text="Property")
vertical_treeview.heading("Value", text="Value")

# Configure the scrollbar to work with the vertical Treeview
vertical_treeview.config(xscrollcommand=horizontal_scrollbar_detail.set)
horizontal_scrollbar_detail.config(command=vertical_treeview.xview)

# Configure the scrollbar to work with the vertical Treeview
vertical_treeview.config(yscrollcommand=vertical_scrollbar_detail.set)
vertical_scrollbar_detail.config(command=vertical_treeview.yview)

# Insert labels to display properties in vertical columns
for col in available_columns_detail:
    vertical_treeview.insert("", "end", values=(col, ""))

# Function to update the values in the vertical columns
def update_vertical_columns(data):
    if data:
        for i, col in enumerate(available_columns_detail):
            value = data[0][i] if i < len(data[0]) else "none"
            vertical_treeview.item(vertical_treeview.get_children()[i], values=(col, value))
    else:
        for i, col in enumerate(available_columns_detail):
            value = vertical_treeview.item(vertical_treeview.get_children()[i], option="values")[1]
            vertical_treeview.item(vertical_treeview.get_children()[i], values=("Value", value))
root.mainloop()
  