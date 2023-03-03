import tkinter as tk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants
from tkinter import filedialog
from datetime import datetime
import json


class App:
    def __init__(self, master):
        self.master = master
        master.title("PyNotes")
        cur_time = datetime.now()
        
        self.start_date_lbl = tk.Label(master, text="Start Date:")
        self.start_date_picker = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        today = datetime.today().strftime('%Y-%m-%d')
        self.start_date_picker.set_date(today)
        self.start_date_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.start_date_picker.grid(row=0, column=1, padx=10, pady=10)


        self.start_time_lbl = tk.Label(master, text="Start Time:")
        self.start_time_picker = SpinTimePickerModern(master)
        self.start_time_picker.addAll(constants.HOURS24)
        self.start_time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040", hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
        self.start_time_picker.configure_separator(bg="#404040", fg="#ffffff")
        self.start_time_picker.set24Hrs(0)
        self.start_time_picker.setMins(0)
        self.start_time_lbl.grid(row=1, column=0, padx=10, pady=10)
        self.start_time_picker.grid(row=1, column=1, padx=10, pady=10)


        self.end_date_lbl = tk.Label(master, text="End Date:")
        self.end_date_picker = DateEntry(master, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_picker.set_date(today)
        self.end_date_lbl.grid(row=2, column=0, padx=10, pady=10)
        self.end_date_picker.grid(row=2, column=1, padx=10, pady=10)

        
        self.end_time_lbl = tk.Label(master, text="End Time:")
        self.end_time_picker = SpinTimePickerModern(master)
        self.end_time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040", hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
        self.end_time_picker.configure_separator(bg="#404040", fg="#ffffff")
        self.end_time_picker.addAll(constants.HOURS24)
        self.end_time_picker.set24Hrs(cur_time.hour)
        self.end_time_picker.setMins(cur_time.minute)
        self.end_time_lbl.grid(row=3, column=0, padx=10, pady=10)
        self.end_time_picker.grid(row=3, column=1, padx=10, pady=10)


        self.update_btn = tk.Button(master, text="Update", command=self.update_date_time)
        self.update_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


        self.folder_path_lbl = tk.Label(master, text="")
        try:
            self.folder_path = json.load(open('data.json', 'r'))['Path']
            self.folder_path_lbl.configure(text=self.folder_path)
        except Exception as e:
            pass
        self.folder_btn = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.folder_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.folder_path_lbl.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


    def update_date_time(self):
        # Convert date and time to Unix timestamp
        st_time = f'{self.start_date_picker.get_date()}-{"-".join([str(elem) for elem in self.start_time_picker.time() if type(elem) == int])}'
        ed_time = f'{self.end_date_picker.get_date()}-{"-".join([str(elem) for elem in self.end_time_picker.time() if type(elem) == int])}'
        
        unix_st = int(datetime.strptime(st_time, '%Y-%m-%d-%H-%M').timestamp())
        unix_ed = int(datetime.strptime(ed_time, '%Y-%m-%d-%H-%M').timestamp())

        self.call_function(unix_st, unix_ed, self.folder_path)

    def call_function(self, start_time, end_time, path):
        # Replace this with your function
        print("Start time:", start_time)
        print("End time:", end_time)
        print(path)

    def select_folder(self):
        # Prompt user to select a folder using file explorer
        self.folder_path = filedialog.askdirectory()
        self.folder_path_lbl.configure(text=self.folder_path)


root = tk.Tk()
app = App(root)
root.mainloop()