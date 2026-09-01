import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os
DB_NAME = "local_car_registry.db"

def initialize_local_db():
    """Creates the SQLite database file and tables on the local system if missing."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT UNIQUE NOT NULL,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            color TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def save_vehicle_locally():
    """Reads input fields, validates data, and saves it directly to the local storage."""
    plate = entry_plate.get().strip().upper()
    make = entry_make.get().strip()
    model = entry_model.get().strip()
    color = entry_color.get().strip()

    # Data Validation
    if not plate or not make or not model or not color:
        messagebox.showerror("Validation Error", "All entry fields must be filled out.")
        return

    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
 
        cursor.execute("""
            INSERT INTO vehicles (license_plate, make, model, color)
            VALUES (?, ?, ?, ?)
        """, (plate, make, model, color))
        
        connection.commit()
        connection.close()
        
        messagebox.showinfo("Success", f"Plate '{plate}' successfully logged to local system.")

        clear_input_fields()
        update_ui_data_grid()
        
    except sqlite3.IntegrityError:
        messagebox.showerror("Database Conflict", f"The plate entry '{plate}' already exists on this machine.")

def clear_input_fields():
    """Clears text characters from all active GUI fields."""
    entry_plate.delete(0, tk.END)
    entry_make.delete(0, tk.END)
    entry_model.delete(0, tk.END)
    entry_color.delete(0, tk.END)

def update_ui_data_grid():
    """Reads historical data matrices from disk and populates the visible data grid."""

    for record in tree.get_children():
        tree.delete(record)
        
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT license_plate, make, model, color FROM vehicles ORDER BY id DESC")
    saved_rows = cursor.fetchall()
    connection.close()
    
  
    for row in saved_rows:
        tree.insert("", tk.END, values=row)


initialize_local_db()


root = tk.Tk()
root.title("Local Vehicle Inventory Logger")
root.geometry("620x520")
root.configure(padx=15, pady=15)

# Input Management Frame
input_group = tk.LabelFrame(root, text=" Local System Data Inputs ", padx=15, pady=15)
input_group.pack(fill="x", pady=(0, 15))


tk.Label(input_group, text="License Plate:").grid(row=0, column=0, sticky="w", pady=4)
entry_plate = tk.Entry(input_group, width=28)
entry_plate.grid(row=0, column=1, pady=4, padx=10)

tk.Label(input_group, text="Car Make:").grid(row=1, column=0, sticky="w", pady=4)
entry_make = tk.Entry(input_group, width=28)
entry_make.grid(row=1, column=1, pady=4, padx=10)

tk.Label(input_group, text="Car Model:").grid(row=2, column=0, sticky="w", pady=4)
entry_model = tk.Entry(input_group, width=28)
entry_model.grid(row=2, column=1, pady=4, padx=10)

tk.Label(input_group, text="Car Color:").grid(row=3, column=0, sticky="w", pady=4)
entry_color = tk.Entry(input_group, width=28)
entry_color.grid(row=3, column=1, pady=4, padx=10)

btn_save = tk.Button(input_group, text="Commit to Storage", command=save_vehicle_locally, bg="#0056b3", fg="white", width=18)
btn_save.grid(row=4, column=1, pady=10, sticky="e", padx=10)


grid_group = tk.LabelFrame(root, text=" Offline Local Storage Viewer ", padx=10, pady=10)
grid_group.pack(fill="both", expand=True)


y_scroll = tk.Scrollbar(grid_group)
y_scroll.pack(side="right", fill="y")

data_columns = ("plate", "make", "model", "color")
tree = ttk.Treeview(grid_group, columns=data_columns, show="headings", yscrollcommand=y_scroll.set)
y_scroll.config(command=tree.yview)


tree.heading("plate", text="License Plate")
tree.heading("make", text="Make")
tree.heading("model", text="Model")
tree.heading("color", text="Color")

tree.column("plate", width=130, anchor="center")
tree.column("make", width=130, anchor="center")
tree.column("model", width=130, anchor="center")
tree.column("color", width=110, anchor="center")

tree.pack(fill="both", expand=True)

update_ui_data_grid()

root.mainloop()
