import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from tkcalendar import DateEntry  
from tkinter import END, ttk

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root@123",
    "database": "dipl_system",
}

def open_view_data_window():
    global current_page 

    def fetch_data(start_date, end_date, selected_columns_str):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = f"SELECT {selected_columns_str} FROM purchase_documents WHERE doc_date BETWEEN %s AND %s"

            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()

            conn.close()
            return data

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")
            return []


    def show_detail(event):
        item = result_treeview.selection()[0]  
        id_value = result_treeview.item(item, "values")[0]  

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = """
            SELECT pd.*, pm.name
            FROM purchase_documents AS pd
            LEFT JOIN party_masters pm ON pd.party_id = pm.id
            WHERE pd.id = %s
            """
            cursor.execute(query, (id_value,))
            data = cursor.fetchall()

            conn.close()

            for item in detail_treeview.get_children():
                detail_treeview.delete(item)

            for row in data:
                detail_treeview.insert("", "end", values=row)

            update_vertical_columns(data)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

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

        offset = (current_page - 1) * items_per_page

        data = fetch_data(start_date, end_date, selected_columns_str)

        if data:
            for item in result_treeview.get_children():
                result_treeview.delete(item)

            for row in data[offset:offset + items_per_page]:
                result_treeview.insert("", "end", values=row)

        else:
            messagebox.showinfo("No Data", "No data found for the specified date range.")

    def next_page():
        global current_page
        current_page += 1
        show_data()

    def previous_page():
        global current_page
        if current_page > 1:
            current_page -= 1
            show_data()

    def update_vertical_columns(data):
        if data:
            for i, col in enumerate(available_columns_detail):
                value = data[0][i] if i < len(data[0]) else "none"
                vertical_treeview.item(vertical_treeview.get_children()[i], values=(col, value))
        else:
            for i, col in enumerate(available_columns_detail):
                value = vertical_treeview.item(vertical_treeview.get_children()[i], option="values")[1]
                vertical_treeview.item(vertical_treeview.get_children()[i], values=("Value", value))

    root_view_data = tk.Toplevel()
    root_view_data.title("View Data")

    start_date_label = ttk.Label(root_view_data, text="Start Date:")
    start_date_label.grid(row=0, column=0, padx=10, pady=(10, 0))

    start_date_entry = DateEntry(root_view_data, date_pattern="yyyy-mm-dd")
    start_date_entry.grid(row=0, column=1, padx=10, pady=(10, 0))

    end_date_label = ttk.Label(root_view_data, text="End Date:")
    end_date_label.grid(row=1, column=0, padx=10)

    end_date_entry = DateEntry(root_view_data, date_pattern="yyyy-mm-dd")
    end_date_entry.grid(row=1, column=1, padx=10)

    available_columns = ["id", "doc_number", "doc_date", "total_amount", "product_category"]
    column_vars = []

    show_button = ttk.Button(root_view_data, text="Show Data", command=show_data)
    show_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    result_treeview = ttk.Treeview(root_view_data, columns=available_columns, show="headings", height=7)

    for col in available_columns:
        result_treeview.heading(col, text=col)
        result_treeview.column(col, width=250)

    result_treeview.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

    next_button = ttk.Button(root_view_data, text="Next Page", command=next_page)
    next_button.grid(row=5, column=0, padx=10, pady=10)

    previous_button = ttk.Button(root_view_data, text="Previous Page", command=previous_page)
    previous_button.grid(row=5, column=1, padx=10, pady=10)

    current_page = 1
    items_per_page = 10

    result_treeview.bind("<Double-1>", show_detail)

    available_columns_detail = [
        "ID", "DOCUMENT_NO", "DOCUMENT_DATE", "PARTY_ID", "PRODUCT_DETAILS", "TOATAL_AMOUNT",
        "PRODUCT_CATEGORY", "DESCRIPTION", "THREAD_SUPPLIER", "COMPANY_ID",
        "CHECKLIST_IDS",  "PDF_FILE", "PD_LOCATION", "REFERENCE_NO", "REFERENCE_SR",
        "STATUS", "CREATED_BY", "CREATED_AT", "UPDATED_AT", "NAME"
    ]

    detail_treeview = ttk.Treeview(root_view_data, columns=available_columns_detail, show="headings", height=2)

    for col in available_columns_detail:
        detail_treeview.heading(col, text=col)
        detail_treeview.column(col, width=65)

    detail_treeview.grid(row=6, column=0, columnspan=2, padx=20, pady=20)

    vertical_frame = ttk.Frame(root_view_data)
    vertical_frame.grid(row=8, column=1, padx=20, pady=20, sticky="nsew")

    vertical_scrollbar_detail = ttk.Scrollbar(vertical_frame, orient="vertical")
    vertical_scrollbar_detail.grid(row=0, column=1, sticky="ns")

    horizontal_scrollbar_detail = ttk.Scrollbar(vertical_frame, orient="horizontal")
    horizontal_scrollbar_detail.grid(row=7, column=0, sticky="ns")

    vertical_treeview = ttk.Treeview(vertical_frame, columns=["Property", "Value"], show="headings", height=10)
    vertical_treeview.grid(row=0, column=0)

    vertical_treeview.heading("Property", text="Property")
    vertical_treeview.heading("Value", text="Value")

    vertical_treeview.config(xscrollcommand=horizontal_scrollbar_detail.set)
    horizontal_scrollbar_detail.config(command=vertical_treeview.xview)

    vertical_treeview.config(yscrollcommand=vertical_scrollbar_detail.set)
    vertical_scrollbar_detail.config(command=vertical_treeview.yview)

    for col in available_columns_detail:
        vertical_treeview.insert("", "end", values=(col, ""))

    root_view_data.mainloop()

window = tk.Tk()
window.title("Add Entry to DIPL SQLyog Database")

def add_entry_and_open_view_data():
    add_entry() 
    open_view_data_window() 
def add_entry():
    doc_number = doc_number_entry.get()
    doc_date = doc_date_entry.get()
    party_id = party_id_entry.get()
    product_details = product_details_entry.get()
    total_amount = total_amount_entry.get()
    product_category = product_category_entry.get()
    description = description_entry.get()
    thread_supplier = thread_supplier_entry.get()
    company_id = company_id_entry.get()
    cheklist_ids = cheklist_ids_entry.get()
    pdf_file = pdf_file_entry.get()
    pd_location = pd_location_entry.get()
    reference_no = reference_no_entry.get()
    reference_sr = reference_sr_entry.get()
    status = status_entry.get()
    created_by = created_by_entry.get()
    
    if not doc_number or not doc_date or not party_id:
        messagebox.showerror("Error", "Document No, Document Date, and Party ID are required fields.")
        return

    try:

        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        table_name = "purchase_documents"

        insert_query = f"""
            INSERT INTO {table_name} (
            doc_number, doc_date, party_id, product_details, total_amount,
            product_category, description, thread_supplier, company_id,
            cheklist_ids, pdf_file, pd_location, reference_no, reference_sr,
            status, created_by, created_at, updated_at) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (
            doc_number, doc_date, party_id, product_details, total_amount,
            product_category, description, thread_supplier, company_id,
            cheklist_ids, pdf_file, pd_location, reference_no, reference_sr,
            status, created_by, timestamp, timestamp
        )
        cursor.execute(insert_query, data)

        connection.commit()
        messagebox.showinfo("Success", "Entry added successfully!") 

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


doc_number_label = tk.Label(window, text="DOCUMENT_NO:")
doc_number_label.pack()
doc_number_entry = tk.Entry(window ,width=100)
doc_number_entry.pack()

doc_date_label = tk.Label(window, text="DOCUMENT_DATE:")
doc_date_label.pack()
doc_date_entry = tk.Entry(window, width=100)
doc_date_entry.pack()

party_id_label = tk.Label(window, text="PARTY_ID:")
party_id_label.pack()
party_id_entry = tk.Entry(window, width=100)
party_id_entry.pack()

product_details_label = tk.Label(window, text=" PRODUCT_DETAILS:")
product_details_label.pack()
product_details_entry = tk.Entry(window, width=100)
product_details_entry.pack()

total_amount_label = tk.Label(window, text=" TOATAL_AMOUNT:")
total_amount_label.pack()
total_amount_entry = tk.Entry(window, width=100)
total_amount_entry.pack()

product_category_label = tk.Label(window, text="PRODUCT_CATEGORY:")
product_category_label.pack()
product_category_entry = tk.Entry(window, width=100)
product_category_entry.pack()

description_label = tk.Label(window, text="DESCRIPTION:")
description_label.pack()
description_entry = tk.Entry(window, width=100)
description_entry.pack()

thread_supplier_label = tk.Label(window, text="THREAD_SUPPLIER:")
thread_supplier_label.pack()
thread_supplier_entry = tk.Entry(window, width=100)
thread_supplier_entry.pack()

company_id_label = tk.Label(window, text="COMPANY_ID:")
company_id_label.pack()
company_id_entry = tk.Entry(window, width=100)
company_id_entry.pack()

cheklist_ids_label = tk.Label(window, text="cheklist_ids:")
cheklist_ids_label.pack()
cheklist_ids_entry = tk.Entry(window, width=100)
cheklist_ids_entry.pack()

pdf_file_label = tk.Label(window, text="PDF_FILE:")
pdf_file_label.pack()
pdf_file_entry = tk.Entry(window, width=100)
pdf_file_entry.pack()

pd_location_label = tk.Label(window, text="PD_LOCATION:")
pd_location_label.pack()
pd_location_entry = tk.Entry(window, width=100)
pd_location_entry.pack()

reference_no_label = tk.Label(window, text="REFERENCE_NO:")
reference_no_label.pack()
reference_no_entry = tk.Entry(window, width=100)
reference_no_entry.pack()

reference_sr_label = tk.Label(window, text="REFERENCE_SR:")
reference_sr_label.pack()
reference_sr_entry = tk.Entry(window, width=100)
reference_sr_entry.pack()

status_label = tk.Label(window, text="STATUS:")
status_label.pack()
status_entry = tk.Entry(window, width=100)
status_entry.pack()

created_by_label = tk.Label(window, text="CREATED_BY:")
created_by_label.pack()
created_by_entry = tk.Entry(window, width=100)
created_by_entry.pack()

add_button = tk.Button(window, text="Add Entry and View Data", command=add_entry_and_open_view_data)
add_button.pack()

window.mainloop()
