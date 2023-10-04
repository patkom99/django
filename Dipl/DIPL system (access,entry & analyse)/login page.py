import tkinter as tk
from tkinter import messagebox
import os

# Function to handle login button click
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Replace this with your authentication logic
    if username == "manoj.newalkar@gmail.com" and password == "secretischanged":
        messagebox.showinfo("Login Successful", "Welcome, " + username)
        open_python_file()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to open the Python file
def open_python_file():
    python_file_path = r"C:/Users/Avinash/Desktop/demo_app/example-app/resources/views/add_data_and_analyse_of_dipl_sy.py"
    
    if os.path.exists(python_file_path):
        os.system("start " + python_file_path)
    else:
        messagebox.showerror("File Not Found", "The specified Python file does not exist.")

# Create the main login window
root = tk.Tk()
root.title("Login Page")

# Username label and entry
label_username = tk.Label(root,  text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

# Password label and entry
label_password = tk.Label(root,text="Password:")
label_password.pack()
entry_password = tk.Entry(root,show="*")  # Show * for password
entry_password.pack()

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

# Run the Tkinter main loop
root.mainloop()
