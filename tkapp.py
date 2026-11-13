import json
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import tkinter.ttk as ttk


with open("students.json") as file:
  students = json.load(file)

studentslist = []
for student in students:
  studentslist.append(f'{student["firstName"]} {student["lastName"]}')
preloaded_student_info={}
for index in range(len(studentslist)):
    preloaded_student_info[studentslist[index]]=students[index]
studentslist.sort()

root = tk.Tk()
# 1. Made the window larger to provide more vertical space
root.geometry("800x700")
root.title("WHHS RosterTk")

# Set comfortable row height
style = ttk.Style()
style.configure("Treeview", rowheight=30)

# Create a frame for the treeview and scrollbars
frame = ttk.Frame(root)
frame.pack(expand=True, fill=BOTH, padx=15, pady=15)

# Define Treeview with columns and a larger explicit height (e.g., 25 visible rows)
tree = ttk.Treeview(
    frame,
    columns=("Name", "Grade"),
    show="headings",
    selectmode="browse",
    height=25,
)

# Hide the default tree column (#0)
tree.column("#0", width=0, stretch=False)

# Configure headings
tree.heading("Name", text="Student Name", anchor="w")
tree.heading("Grade", text="Grade", anchor="w")

# Column width configuration
tree.column("Name", width=500, stretch=True, anchor="w")
tree.column("Grade", width=150, stretch=True, anchor="w")

# Add vertical and horizontal scrollbars
vsbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
hsbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsbar.set, xscrollcommand=hsbar.set)

for i in range(len(studentslist)):
  name = (
      studentslist[i % len(studentslist)]
      if studentslist
      else f"Student {i}"
  )
  grade = preloaded_student_info[name]['grade']
  tree.insert("", "end", values=(name, grade))

# Grid layout for tree and scrollbars
tree.grid(row=1, column=0, sticky="nsew")
vsbar.grid(row=1, column=1, sticky="ns")
hsbar.grid(row=2, column=0, sticky="ew")

frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

search_entry=ttk.Entry(frame)
search_entry.grid(row=0,column=0,sticky="ew")
search_btn=ttk.Button(frame,text="Search")
search_btn.grid(row=0,column=1,sticky="ew")

# Handle row selection
def on_row_select(event):
  selected_item = tree.selection()
  if selected_item:
    item_values = tree.item(selected_item, "values")
    messagebox.showinfo("WHHS Roster", f"{item_values[0]}\nGrade: {preloaded_student_info[item_values[0]]['grade']}")


tree.bind("<<TreeviewSelect>>", on_row_select)

root.mainloop()
