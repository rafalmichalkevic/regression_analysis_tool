import tkinter as tk
from tkinter import filedialog
import os

class Window:
    APP_TITLE = "Regression analyser"

    def __init__(self, width, height):
        self.app = tk.Tk()
        self.width = width
        self.height = height
        self._configure_window()

    def _browse_file(self):
        file_path = filedialog.askopenfilename(title="Select a .py File", filetypes=[("Python Files", "*.py")])
        filename = os.path.basename(file_path)
        self.filepath_label_var.set(f"File Path: .../{filename}")
        return file_path

    def _create_menu(self):
        menu_bar = tk.Menu(self.app)
        self.app.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open", command=self._browse_file)
            
    def _add_labels(self):
        self.filepath_label_var = tk.StringVar(value="File Path: ")
        filepath_label = tk.Label(self.app, textvariable=self.filepath_label_var)
        filepath_label.pack()

        self.selected_file_var = tk.StringVar()
        selected_file_entry = tk.Entry(self.app, textvariable=self.selected_file_var)
        selected_file_entry.pack()

    def _configure_window(self):
        self.app.title(self.APP_TITLE)
        self.app.geometry(f"{self.width}x{self.height}")
        self.app.resizable(True, True)
        self._create_menu()
        self._add_labels()
        
    def run(self):
        self.app.mainloop()