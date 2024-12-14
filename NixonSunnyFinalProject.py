"""
finalproject.py
 Author: Sunny Nixon
 Date written: 12/01/24
 Assignment: Final
Necessities:
The link of the GitHub repository for your final project. 10 points
A working GUI tkinter application with at least two windows. 50 points
Implementing a modular approach in your application. 10 points
Consistent clear navigation throughout the GUI application. 10 points
Use at least two images in your application(images should have alternate text). 10 points
Include at least three labels. 10 points
Include at least three buttons. 10 points
Include at least three call back function with each button, including exit button. 20 points
Implement secure coding best practices, including input validation to check if the user 
entered the correct data type, make sure the entry box is not empty, etc. 10 points
"""
# I am using tkinter, pyhton pillow, and python pip
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json

class TodoList(tk.Tk):
    def __init__(self):
        super().__init__()

# This sets the title and window size for the main window, opened firtst
        self.title("Todo List-Python Final")
        self.geometry("500x800")  

# This resizes the image for the todo list icon of a notepad
        self.image = Image.open("list.png")  
        self.image = self.image.resize((200, 200))  
        self.photo = ImageTk.PhotoImage(self.image)

# This will create a label in order to display the image in the main window
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(pady=10)  

# This text is for accessability, it creates a label for the displayed image
        self.alt_text = "Above is a placeholder image for the Todo List application of a notepad and pencil."
        self.alt_text_label = tk.Label(self, text=self.alt_text, font=("TkDefaultFont", 12), wraplength=300)
        self.alt_text_label.pack(pady=5)

# Tooltip for the image
        self.create_tooltip(self.image_label, "This image represents the Todo List app interface.")

# Field given to input information/tasks for your list
        self.task_input = ttk.Entry(self, font=("TkDefaultFont", 16), width=30, style="Custom.TEntry")
        self.task_input.pack(pady=10)

        self.task_input.insert(0, "Enter a todo here...")

# Handles the placeholder text
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

# Adds an "add" button in order to insert tasks onto the list
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

# Creates the actual list box
        self.task_list = tk.Listbox(self, font=("TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Creates the "done", "delete", "view stats", and "quit" buttons
        ttk.Button(self, text="Done", style="success.TButton", 
                   command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton", 
                   command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)

        ttk.Button(self, text="View Stats", style="info.TButton", command=self.view_stats).pack(side=tk.BOTTOM, pady=10)

        tk.Button(self, text="Quit", command=self.destroy).pack(pady=5)

# load any saved files
        self.load_tasks()

# this is for the stats button and window. you can see the completed tasks for it. this involves a counter for completed tasks.
    def view_stats(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1

# creates a new window for task stats
        stats_window = tk.Toplevel(self)
        stats_window.title("Task Statistics")
        stats_window.geometry("300x350")
        stats_window.grab_set() 

# this loads and displays the image of the sticky note given
        image = Image.open("stickynote.png")
        image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(image)

        alt_text = "Below is a placeholder image of a sticky note for your task statistics."
        alt_text_label = tk.Label(stats_window, text=alt_text, font=("TkDefaultFont", 10), wraplength=250)
        alt_text_label.pack(pady=5)

        image_label = tk.Label(stats_window, image=photo)
        image_label.image = photo
        image_label.pack(pady=10)

# this will display the stats given in the task stat window
        stats_text = f"Total tasks: {total_count}\nCompleted tasks: {done_count}"
        stats_label = tk.Label(stats_window, text=stats_text, font=("TkDefaultFont", 12))
        stats_label.pack(pady=10)

# button used to close the task stat window
        ttk.Button(stats_window, text="Close", command=stats_window.destroy).pack(pady=10)

# this is used to add new tasks to the list and sets the text color to orange before being turned green for completion. this will also save the tasks given
    def add_task(self):
        task = self.task_input.get()
        if task != "Enter your todo here...":
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.task_input.delete(0, tk.END)
            self.save_tasks()

# used to mark the task as done
    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            self.save_tasks()

#used to delete the selected task when selected and save the data afterwards
    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()

# used to clear any text in the input field, also known as resetting the input field as blank
    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter a todo here...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

# can restore the text if the field is empty
    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter your todo here...")
            self.task_input.configure(style="Custom.TEntry")

# used to load from the saved file, json
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass

# this saves the current tasks to the json file and gives the text and text color 
    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

# gives and hides tooltips needed
    def create_tooltip(self, widget, text):
        tooltip = tk.Label(self, text=text, background="black", relief="solid", borderwidth=1, font=("TkDefaultFont", 10))
        tooltip.place_forget() 

# displays the tool tip when hovered on
        def on_enter(event):
            tooltip.place(x=event.x_root, y=event.y_root)

        def on_leave(event):
            tooltip.place_forget()

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

# main entry for app and runs the app
if __name__ == '__main__':
    app = TodoList()
    app.mainloop()
