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
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json

class TodoList(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Todo List-Python Final")
        self.geometry("500x800")  


        self.image = Image.open("list.png")  
        self.image = self.image.resize((200, 200))  
        self.photo = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(pady=10)  

        self.alt_text = "Above is a placeholder image for the Todo List application of a notepad and pencil."
        self.alt_text_label = tk.Label(self, text=self.alt_text, font=("TkDefaultFont", 12), wraplength=300)
        self.alt_text_label.pack(pady=5)

        self.create_tooltip(self.image_label, "This image represents the Todo List app interface.")

        self.task_input = ttk.Entry(self, font=("TkDefaultFont", 16), width=30, style="Custom.TEntry")
        self.task_input.pack(pady=10)

        self.task_input.insert(0, "Enter a todo here...")

        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        self.task_list = tk.Listbox(self, font=("TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(self, text="Done", style="success.TButton", 
                   command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton", 
                   command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)

        ttk.Button(self, text="View Stats", style="info.TButton", command=self.view_stats).pack(side=tk.BOTTOM, pady=10)

        tk.Button(self, text="Quit", command=self.destroy).pack(pady=5)

        self.load_tasks()

    def view_stats(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1

        stats_window = tk.Toplevel(self)
        stats_window.title("Task Statistics")
        stats_window.geometry("300x350")
        stats_window.grab_set() 

        image = Image.open("stickynote.png")
        image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(image)

        alt_text = "Below is a placeholder image of a sticky note for your task statistics."
        alt_text_label = tk.Label(stats_window, text=alt_text, font=("TkDefaultFont", 10), wraplength=250)
        alt_text_label.pack(pady=5)

        image_label = tk.Label(stats_window, image=photo)
        image_label.image = photo
        image_label.pack(pady=10)

        stats_text = f"Total tasks: {total_count}\nCompleted tasks: {done_count}"
        stats_label = tk.Label(stats_window, text=stats_text, font=("TkDefaultFont", 12))
        stats_label.pack(pady=10)

        ttk.Button(stats_window, text="Close", command=stats_window.destroy).pack(pady=10)

    def add_task(self):
        task = self.task_input.get()
        if task != "Enter your todo here...":
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.task_input.delete(0, tk.END)
            self.save_tasks()

    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            self.save_tasks()

    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()

    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter a todo here...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter your todo here...")
            self.task_input.configure(style="Custom.TEntry")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass

    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

    def create_tooltip(self, widget, text):
        tooltip = tk.Label(self, text=text, background="yellow", relief="solid", borderwidth=1, font=("TkDefaultFont", 10))
        tooltip.place_forget() 

        def on_enter(event):
            tooltip.place(x=event.x_root, y=event.y_root)

        def on_leave(event):
            tooltip.place_forget()

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

if __name__ == '__main__':
    app = TodoList()
    app.mainloop()


